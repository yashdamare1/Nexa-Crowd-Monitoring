from risk_config import RiskConfig
from risk_level import RiskLevel


class RiskEvaluator:
    """
    Evaluates crowd risk using the configured thresholds.
    """

    def __init__(self, config: RiskConfig):
        self.config = config

    def evaluate(self, people_count: int) -> RiskLevel:

        if people_count >= self.config.critical_threshold:
            return RiskLevel.CRITICAL

        if people_count >= self.config.warning_threshold:
            return RiskLevel.WARNING

        return RiskLevel.NORMAL