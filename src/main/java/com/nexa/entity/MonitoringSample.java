package com.nexa.entity;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "monitoring_samples")
public class MonitoringSample {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, length = 100)
    private String sourceId;

    @Column(nullable = false)
    private Integer personCount;

    @Column(nullable = false, length = 20)
    private String riskLevel;

    @Column(nullable = false)
    private Boolean sourceOnline;

    @Column(nullable = false)
    private LocalDateTime recordedAt;

    public MonitoringSample() {
    }

    public Long getId() {
        return id;
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

    public LocalDateTime getRecordedAt() {
        return recordedAt;
    }

    public void setRecordedAt(LocalDateTime recordedAt) {
        this.recordedAt = recordedAt;
    }
}