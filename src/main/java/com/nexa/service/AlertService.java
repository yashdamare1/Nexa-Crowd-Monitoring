package com.nexa.service;

import com.nexa.entity.Alert;
import com.nexa.repository.AlertRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Locale;

@Service
public class AlertService {

    private final AlertRepository alertRepository;

    public AlertService(AlertRepository alertRepository) {
        this.alertRepository = alertRepository;
    }

    @Transactional
    public Alert saveAlert(Alert alert) {
        if (alert.getSourceAlertId() == null ||
                alert.getPipelineRunId() == null ||
                alert.getPipelineRunId().isBlank() ||
                alert.getSourceId() == null ||
                alert.getSourceId().isBlank() ||
                alert.getEventType() == null ||
                alert.getRiskLevel() == null ||
                alert.getMessage() == null ||
                alert.getStatus() == null ||
                alert.getCreatedAt() == null) {
            throw new IllegalArgumentException(
                    "Required alert fields must not be empty"
            );
        }

        alert.setSourceId(alert.getSourceId().trim());
        alert.setPipelineRunId(alert.getPipelineRunId().trim());
        alert.setEventType(alert.getEventType().toUpperCase(Locale.ROOT));
        alert.setRiskLevel(alert.getRiskLevel().toUpperCase(Locale.ROOT));
        alert.setStatus(alert.getStatus().toUpperCase(Locale.ROOT));

        if (!List.of("CREATED", "ESCALATED", "RESOLVED")
                .contains(alert.getEventType())) {
            throw new IllegalArgumentException("Invalid alert event type");
        }

        if (!List.of("NORMAL", "WARNING", "CRITICAL")
                .contains(alert.getRiskLevel())) {
            throw new IllegalArgumentException("Invalid risk level");
        }

        if (!List.of("ACTIVE", "RESOLVED").contains(alert.getStatus())) {
            throw new IllegalArgumentException("Invalid alert status");
        }

        if ("RESOLVED".equals(alert.getEventType())) {
            if (!"RESOLVED".equals(alert.getStatus()) ||
                    alert.getResolvedAt() == null) {
                throw new IllegalArgumentException(
                        "Resolved events require RESOLVED status and resolvedAt"
                );
            }
        } else if (!"ACTIVE".equals(alert.getStatus()) ||
                alert.getResolvedAt() != null) {
            throw new IllegalArgumentException(
                    "CREATED and ESCALATED events must be ACTIVE and unresolved"
            );
        }

        return alertRepository
                .findBySourceIdAndPipelineRunIdAndSourceAlertIdAndEventType(
                        alert.getSourceId(),
                        alert.getPipelineRunId(),
                        alert.getSourceAlertId(),
                        alert.getEventType()
                )
                .orElseGet(() -> alertRepository.save(alert));
    }

    public List<Alert> getAllAlerts() {
        return alertRepository.findAllByOrderByCreatedAtDesc();
    }

    public List<Alert> getAlertsBySource(String sourceId) {
        return alertRepository.findBySourceIdOrderByCreatedAtDesc(sourceId);
    }

    public List<Alert> getAlertsByStatus(String status) {
        return alertRepository.findByStatusOrderByCreatedAtDesc(
                status.toUpperCase(Locale.ROOT)
        );
    }
}