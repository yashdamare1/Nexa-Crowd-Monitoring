
package com.nexa.service;

import com.nexa.dto.MonitoringUpdateRequest;
import com.nexa.entity.MonitoringSample;
import com.nexa.entity.MonitoringSource;
import com.nexa.repository.MonitoringSampleRepository;
import com.nexa.repository.MonitoringSourceRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.Comparator;
import java.util.List;

@Service
public class MonitoringService {

    private final MonitoringSourceRepository repository;
    private final MonitoringSampleRepository sampleRepository;

    public MonitoringService(
            MonitoringSourceRepository repository,
            MonitoringSampleRepository sampleRepository) {
        this.repository = repository;
        this.sampleRepository = sampleRepository;
    }

    @Transactional
    public MonitoringState update(MonitoringUpdateRequest request) {
        String sourceId = request.getSourceId().trim();
        LocalDateTime now = LocalDateTime.now();

        MonitoringSource source = repository.findById(sourceId)
                .orElseGet(MonitoringSource::new);

        source.setSourceId(sourceId);
        source.setPersonCount(request.getPersonCount());
        source.setRiskLevel(
                request.getRiskLevel().trim().toUpperCase()
        );
        source.setSourceOnline(request.getSourceOnline());
        source.setLastUpdated(now);

        MonitoringSource saved = repository.save(source);

        MonitoringSample sample = new MonitoringSample();
        sample.setSourceId(sourceId);
        sample.setPersonCount(request.getPersonCount());
        sample.setRiskLevel(
                request.getRiskLevel().trim().toUpperCase()
        );
        sample.setSourceOnline(request.getSourceOnline());
        sample.setRecordedAt(now);

        sampleRepository.save(sample);

        return toState(saved);
    }

    @Transactional(readOnly = true)
    public List<MonitoringState> getAllSources() {
        return repository.findAll()
                .stream()
                .map(MonitoringService::toState)
                .sorted(Comparator.comparing(
                        MonitoringState::getSourceId
                ))
                .toList();
    }

    @Transactional(readOnly = true)
    public MonitoringState getSource(String sourceId) {
        return repository.findById(sourceId)
                .map(MonitoringService::toState)
                .orElse(null);
    }

    @Transactional(readOnly = true)
    public List<MonitoringSample> getRecentSamples(String sourceId) {
        return sampleRepository
                .findTop100BySourceIdOrderByRecordedAtDesc(sourceId)
                .stream()
                .sorted(Comparator.comparing(
                        MonitoringSample::getRecordedAt
                ))
                .toList();
    }

    private static MonitoringState toState(MonitoringSource source) {
        MonitoringState state = new MonitoringState();

        state.setSourceId(source.getSourceId());
        state.setPersonCount(source.getPersonCount());
        state.setRiskLevel(source.getRiskLevel());
        state.setSourceOnline(source.getSourceOnline());
        state.setLastUpdated(source.getLastUpdated());

        return state;
    }

    public static class MonitoringState {

        private String sourceId;
        private Integer personCount;
        private String riskLevel;
        private Boolean sourceOnline;
        private LocalDateTime lastUpdated;

        public MonitoringState() {
        }

        public String getSourceId() {
            return sourceId;
        }

        public void setSourceId(String sourceId) {
            this.sourceId = sourceId;
        }

        public Integer getPersonCount() {
            return personCount;
        }

        public void setPersonCount(Integer personCount) {
            this.personCount = personCount;
        }

        public String getRiskLevel() {
            return riskLevel;
        }

        public void setRiskLevel(String riskLevel) {
            this.riskLevel = riskLevel;
        }

        public Boolean getSourceOnline() {
            return sourceOnline;
        }

        public void setSourceOnline(Boolean sourceOnline) {
            this.sourceOnline = sourceOnline;
        }

        public LocalDateTime getLastUpdated() {
            return lastUpdated;
        }

        public void setLastUpdated(LocalDateTime lastUpdated) {
            this.lastUpdated = lastUpdated;
        }
    }
}
