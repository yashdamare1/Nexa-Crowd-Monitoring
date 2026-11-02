
package com.nexa.repository;

import com.nexa.entity.Alert;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.Optional;

public interface AlertRepository extends JpaRepository<Alert, Long> {

    List<Alert> findAllByOrderByCreatedAtDesc();

    List<Alert> findBySourceIdOrderByCreatedAtDesc(String sourceId);

    List<Alert> findByStatusOrderByCreatedAtDesc(String status);

   Optional<Alert> findBySourceIdAndPipelineRunIdAndSourceAlertIdAndEventType(
    String sourceId,
    String pipelineRunId,
    Long sourceAlertId,
    String eventType
);
}
