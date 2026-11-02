
package com.nexa.controller;

import com.nexa.dto.MonitoringUpdateRequest;
import com.nexa.service.MonitoringService;
import com.nexa.service.MonitoringService.MonitoringState;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/security/monitoring")
public class MonitoringController {

    private final MonitoringService monitoringService;

    public MonitoringController(MonitoringService monitoringService) {
        this.monitoringService = monitoringService;
    }

    @PostMapping("/updates")
    @PreAuthorize("hasAnyRole('ADMIN', 'SECURITY')")
    public ResponseEntity<MonitoringState> receiveUpdate(
            @Valid @RequestBody MonitoringUpdateRequest request) {

        MonitoringState state = monitoringService.update(request);

        return ResponseEntity.status(HttpStatus.CREATED).body(state);
    }

    @GetMapping("/sources")
    @PreAuthorize("hasAnyRole('ADMIN', 'SECURITY')")
    public ResponseEntity<List<MonitoringState>> getAllSources() {
        return ResponseEntity.ok(monitoringService.getAllSources());
    }

    @GetMapping("/sources/{sourceId}")
    @PreAuthorize("hasAnyRole('ADMIN', 'SECURITY')")
    public ResponseEntity<?> getSource(@PathVariable String sourceId) {
        MonitoringState state = monitoringService.getSource(sourceId);

        if (state == null) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND)
                    .body(Map.of("message", "Monitoring source not found"));
        }

        return ResponseEntity.ok(state);
    }
}
