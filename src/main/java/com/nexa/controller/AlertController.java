
package com.nexa.controller;

import com.nexa.entity.Alert;
import com.nexa.service.AlertService;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/security/alerts")
public class AlertController {

    private final AlertService alertService;

    public AlertController(AlertService alertService) {
        this.alertService = alertService;
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public Alert createAlert(@RequestBody Alert alert) {
        return alertService.saveAlert(alert);
    }

    @GetMapping
    public List<Alert> getAllAlerts() {
        return alertService.getAllAlerts();
    }

    @GetMapping("/source/{sourceId}")
    public List<Alert> getAlertsBySource(@PathVariable String sourceId) {
        return alertService.getAlertsBySource(sourceId);
    }

    @GetMapping("/status/{status}")
    public List<Alert> getAlertsByStatus(@PathVariable String status) {
        return alertService.getAlertsByStatus(status.toUpperCase());
    }
}
