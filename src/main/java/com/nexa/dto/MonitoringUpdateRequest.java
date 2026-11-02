package com.nexa.dto;

import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

public class MonitoringUpdateRequest {

    @NotBlank(message = "Source ID is required")
    private String sourceId;

    @NotNull(message = "Person count is required")
    @Min(value = 0, message = "Person count cannot be negative")
    private Integer personCount;

    @NotBlank(message = "Risk level is required")
    private String riskLevel;

    @NotNull(message = "Source online status is required")
    private Boolean sourceOnline;

    public MonitoringUpdateRequest() {
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
}