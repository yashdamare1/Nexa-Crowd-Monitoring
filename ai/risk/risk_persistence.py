from risk_level import RiskLevel


class RiskPersistence:
    """
    Confirms risk escalation quickly but requires
    longer stability before recovering to a lower risk.
    """

    def __init__(
        self,
        escalation_count: int = 3,
        recovery_count: int = 10
    ):
        self.escalation_count = escalation_count
        self.recovery_count = recovery_count

        self.confirmed_level = RiskLevel.NORMAL

        self.pending_level = None
        self.consecutive_count = 0

    def update(
        self,
        risk_level: RiskLevel
    ) -> tuple[RiskLevel, bool]:

        # Current confirmed level remains unchanged.
        if risk_level == self.confirmed_level:

            self.pending_level = None
            self.consecutive_count = 0

            return self.confirmed_level, True

        # New transition started.
        if risk_level != self.pending_level:

            self.pending_level = risk_level
            self.consecutive_count = 1

        else:

            self.consecutive_count += 1

        # --------------------------------
        # Escalation
        # --------------------------------

        if self._is_higher_risk(
            risk_level,
            self.confirmed_level
        ):

            required_count = self.escalation_count

        # --------------------------------
        # Recovery
        # --------------------------------

        else:

            required_count = self.recovery_count

        # --------------------------------
        # Confirm transition
        # --------------------------------

        if self.consecutive_count >= required_count:

            self.confirmed_level = self.pending_level

            self.pending_level = None
            self.consecutive_count = 0

            return self.confirmed_level, True

        return self.confirmed_level, False

    def _is_higher_risk(
        self,
        new_level: RiskLevel,
        current_level: RiskLevel
    ) -> bool:

        priority = {
            RiskLevel.NORMAL: 0,
            RiskLevel.WARNING: 1,
            RiskLevel.CRITICAL: 2
        }

        return (
            priority[new_level]
            > priority[current_level]
        )