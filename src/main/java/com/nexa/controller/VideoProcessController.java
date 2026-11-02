
package com.nexa.controller;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;
import java.util.Map;
import java.util.concurrent.TimeUnit;
import java.util.stream.Stream;

@RestController
@RequestMapping("/api/security/video")
public class VideoProcessController {

    private final Path projectRoot =
            Paths.get("").toAbsolutePath().normalize();

    private final Path videoDirectory =
            projectRoot.resolve("ai/video").normalize();

    private final Path pythonExecutable =
            projectRoot.resolve("ai/.venv/Scripts/python.exe").normalize();

    private final Path detectionScript =
            projectRoot.resolve("ai/detection/video_alert_test.py").normalize();

    private Process pipelineProcess;
    private String selectedVideo;

    @GetMapping("/videos")
    public List<String> getVideos() {
        if (!Files.isDirectory(videoDirectory)) {
            throw new ResponseStatusException(
                    HttpStatus.INTERNAL_SERVER_ERROR,
                    "Video directory was not found.");
        }

        try (Stream<Path> files = Files.list(videoDirectory)) {
            return files
                    .filter(Files::isRegularFile)
                    .map(path -> path.getFileName().toString())
                    .filter(name -> {
                        String lower = name.toLowerCase();
                        return lower.endsWith(".mp4")
                                || lower.endsWith(".avi")
                                || lower.endsWith(".mov")
                                || lower.endsWith(".mkv");
                    })
                    .sorted()
                    .toList();
        } catch (IOException exception) {
            throw new ResponseStatusException(
                    HttpStatus.INTERNAL_SERVER_ERROR,
                    "Could not list video files.");
        }
    }

    @PostMapping("/start")
    public synchronized Map<String, String> start(
            @RequestBody Map<String, String> request) {

        if (pipelineProcess != null && pipelineProcess.isAlive()) {
            throw new ResponseStatusException(
                    HttpStatus.CONFLICT,
                    "Video pipeline is already running.");
        }

        String filename = request.get("filename");
        String email = request.get("email");
        String password = request.get("password");

        if (filename == null || filename.isBlank()
                || email == null || email.isBlank()
                || password == null || password.isBlank()) {
            throw new ResponseStatusException(
                    HttpStatus.BAD_REQUEST,
                    "Video filename, email and password are required.");
        }

        Path videoPath = videoDirectory.resolve(filename).normalize();

        boolean supportedVideo = filename.toLowerCase().endsWith(".mp4")
                || filename.toLowerCase().endsWith(".avi")
                || filename.toLowerCase().endsWith(".mov")
                || filename.toLowerCase().endsWith(".mkv");

        if (!videoPath.startsWith(videoDirectory)
                || !videoPath.getFileName().toString().equals(filename)
                || !supportedVideo
                || !Files.isRegularFile(videoPath)
                || !Files.isReadable(videoPath)
                || !Files.isRegularFile(pythonExecutable)
                || !Files.isRegularFile(detectionScript)) {
            throw new ResponseStatusException(
                    HttpStatus.BAD_REQUEST,
                    "Invalid video or pipeline configuration.");
        }

        try {
            ProcessBuilder builder = new ProcessBuilder(
                    pythonExecutable.toString(),
                    detectionScript.toString(),
                    videoPath.toString()
            );

            builder.directory(projectRoot.toFile());
            builder.redirectErrorStream(true);
            builder.redirectOutput(
                    ProcessBuilder.Redirect.appendTo(
                            projectRoot.resolve(
                                    "launcher/video-pipeline.log").toFile()
                    )
            );

            builder.environment().put("NEXA_EMAIL", email);
            builder.environment().put("NEXA_PASSWORD", password);

            pipelineProcess = builder.start();
            selectedVideo = filename;

            return Map.of(
                    "status", "STARTED",
                    "filename", selectedVideo
            );

        } catch (IOException exception) {
            pipelineProcess = null;
            selectedVideo = null;

            throw new ResponseStatusException(
                    HttpStatus.INTERNAL_SERVER_ERROR,
                    "Could not start the video pipeline.");
        }
    }

    @PostMapping("/stop")
    public synchronized Map<String, String> stop() {
        if (pipelineProcess == null || !pipelineProcess.isAlive()) {
            pipelineProcess = null;
            selectedVideo = null;

            return Map.of("status", "NOT_RUNNING");
        }

        pipelineProcess.destroy();

        try {
            if (!pipelineProcess.waitFor(5, TimeUnit.SECONDS)) {
                pipelineProcess.destroyForcibly();
                pipelineProcess.waitFor(3, TimeUnit.SECONDS);
            }
        } catch (InterruptedException exception) {
            Thread.currentThread().interrupt();
            pipelineProcess.destroyForcibly();
        }

        pipelineProcess = null;
        selectedVideo = null;

        return Map.of("status", "STOPPED");
    }

    @GetMapping("/status")
    public synchronized Map<String, String> status() {
        boolean running =
                pipelineProcess != null && pipelineProcess.isAlive();

        if (!running) {
            pipelineProcess = null;
            selectedVideo = null;
        }

        return Map.of(
                "status", running ? "RUNNING" : "STOPPED",
                "filename", selectedVideo == null ? "" : selectedVideo
        );
    }
}
