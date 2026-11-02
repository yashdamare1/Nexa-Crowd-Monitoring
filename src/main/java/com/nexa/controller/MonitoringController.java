
package com.nexa.controller;

import com.nexa.dto.MonitoringUpdateRequest;
import com.nexa.entity.MonitoringSample;
import com.nexa.service.MonitoringService;
import com.nexa.service.MonitoringService.MonitoringState;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

import java.util.List;

@RestController
@RequestMapping("/api/security/monitoring")
public class MonitoringController {

    private final MonitoringService monitoringService;

    public MonitoringController(MonitoringService monitoringService) {
        this.monitoringService = monitoringService;
    }

    @PostMapping("/updates")
    @ResponseStatus(HttpStatus.OK)
    public MonitoringState receiveUpdate(
            @Valid @RequestBody MonitoringUpdateRequest request) {
        return monitoringService.update(request);
    }

    @GetMapping("/sources")
    public List<MonitoringState> getSources() {
        return monitoringService.getAllSources();
    }

    @GetMapping("/sources/{sourceId}")
    public MonitoringState getSource(@PathVariable String sourceId) {
        MonitoringState source = monitoringService.getSource(sourceId);

        if (source == null) {
            throw new ResponseStatusException(
                    HttpStatus.NOT_FOUND,
                    "Monitoring source not found: " + sourceId
            );
        }

        return source;
    }

    @GetMapping("/sources/{sourceId}/history")
    public List<MonitoringSample> getSourceHistory(
            @PathVariable String sourceId) {

        MonitoringState source = monitoringService.getSource(sourceId);

        if (source == null) {
            throw new ResponseStatusException(
                    HttpStatus.NOT_FOUND,
                    "Monitoring source not found: " + sourceId
            );
        }

        return monitoringService.getRecentSamples(sourceId);
    }
}
