
package com.nexa.service;

import com.nexa.dto.MonitoringUpdateRequest;
import org.springframework.stereotype.Service;

import java.time.Instant;
import java.util.Comparator;
import java.util.List;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ConcurrentMap;

@Service
public class MonitoringService {

    private final ConcurrentMap<String, MonitoringState> sources =
            new ConcurrentHashMap<>();

    public MonitoringState update(MonitoringUpdateRequest request) {
        MonitoringState state = new MonitoringState(
                request.getSourceId(),
                request.getPersonCount(),
                request.getRiskLevel(),
                request.getSourceOnline(),
                Instant.now()
        );

        sources.put(request.getSourceId(), state);
        return state;
    }

    public List<MonitoringState> getAllSources() {
        return sources.values()
                .stream()
                .sorted(Comparator.comparing(MonitoringState::getSourceId))
                .toList();
    }

    public MonitoringState getSource(String sourceId) {
        return sources.get(sourceId);
    }

    public static class MonitoringState {

        private final String sourceId;
        private final int personCount;
        private final String riskLevel;
        private final boolean sourceOnline;
        private final Instant updatedAt;

        public MonitoringState(
                String sourceId,
                int personCount,
                String riskLevel,
                boolean sourceOnline,
                Instant updatedAt) {
            this.sourceId = sourceId;
            this.personCount = personCount;
            this.riskLevel = riskLevel;
            this.sourceOnline = sourceOnline;
            this.updatedAt = updatedAt;
        }

        public String getSourceId() {
            return sourceId;
        }

        public int getPersonCount() {
            return personCount;
        }

        public String getRiskLevel() {
            return riskLevel;
        }

        public boolean isSourceOnline() {
            return sourceOnline;
        }

        public Instant getUpdatedAt() {
            return updatedAt;
        }
    }
}
