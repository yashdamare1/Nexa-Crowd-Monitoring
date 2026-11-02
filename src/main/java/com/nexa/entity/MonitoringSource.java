package com.nexa.entity;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "monitoring_sources")
public class MonitoringSource {

    @Id
    @Column(nullable = false, length = 100)
    private String sourceId;

    @Column(nullable = false)
    private Integer personCount;

    @Column(nullable = false, length = 20)
    private String riskLevel;

    @Column(nullable = false)
    private Boolean sourceOnline;

    @Column(nullable = false)
    private LocalDateTime lastUpdated;

    public MonitoringSource() {
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