package com.nexa.repository;

import com.nexa.entity.MonitoringSource;
import org.springframework.data.jpa.repository.JpaRepository;

public interface MonitoringSourceRepository
        extends JpaRepository<MonitoringSource, String> {
}