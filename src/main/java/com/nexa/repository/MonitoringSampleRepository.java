package com.nexa.repository;

import com.nexa.entity.MonitoringSample;
import org.springframework.data.jpa.repository.JpaRepository;

import java.time.LocalDateTime;
import java.util.List;

public interface MonitoringSampleRepository
        extends JpaRepository<MonitoringSample, Long> {

    List<MonitoringSample> findBySourceIdAndRecordedAtAfterOrderByRecordedAtAsc(
            String sourceId,
            LocalDateTime recordedAt
    );

    List<MonitoringSample> findTop100BySourceIdOrderByRecordedAtDesc(
            String sourceId
    );
}