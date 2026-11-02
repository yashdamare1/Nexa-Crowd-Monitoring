from dataclasses import dataclass


@dataclass(frozen=True)
class RiskConfig:
    """
    Threshold configuration for crowd risk evaluation.
    """

    warning_threshold: int
    critical_threshold: int