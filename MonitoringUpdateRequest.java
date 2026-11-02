
package com.nexa.dto;

import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Pattern;

public class MonitoringUpdateRequest {

    @NotBlank(message = "Source ID is required")
    private String sourceId;

    @Min(value = 0, message = "Person count cannot be negative")
    private int personCount;

    @NotNull(message = "Risk level is required")
    @Pattern(
            regexp = "NORMAL|WARNING|CRITICAL",
            message = "Risk level must be NORMAL, WARNING, or CRITICAL"
    )
    private String riskLevel;

    @NotNull(message = "Source status is required")
    private Boolean sourceOnline;

    public MonitoringUpdateRequest() {
    }

    public String getSourceId() {
        return sourceId;
    }

    public void setSourceId(String sourceId) {
        this.sourceId = sourceId;
    }

    public int getPersonCount() {
        return personCount;
    }

    public void setPersonCount(int personCount) {
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
