from datetime import datetime

from alert import Alert
from alert_status import AlertStatus


class AlertEngine:
    """
    Creates and manages crowd-risk alerts.

    Only one alert can remain active at a time.
    """

    def __init__(self):
        self.active_alert = None
        self.next_alert_id = 1

    def process(self, risk_level: str):

        # --------------------------------
        # NORMAL
        # --------------------------------

        if risk_level == "NORMAL":

            if self.active_alert is not None:

                self.active_alert.status = (
                    AlertStatus.RESOLVED
                )

                self.active_alert.resolved_at = (
                    datetime.now()
                )

                resolved_alert = self.active_alert

                self.active_alert = None

                return {
                    "event": "RESOLVED",
                    "alert": resolved_alert
                }

            return None

        # --------------------------------
        # WARNING / CRITICAL
        # --------------------------------

        if self.active_alert is not None:

            # Escalate existing alert.
            if (
                risk_level == "CRITICAL"
                and self.active_alert.risk_level == "WARNING"
            ):

                self.active_alert.risk_level = "CRITICAL"

                self.active_alert.message = (
                    "Crowd risk escalated to CRITICAL"
                )

                return {
                    "event": "ESCALATED",
                    "alert": self.active_alert
                }

            # Existing alert remains active.
            return None

        # --------------------------------
        # Create new alert
        # --------------------------------

        alert = Alert(
            alert_id=self.next_alert_id,
            risk_level=risk_level,
            message=(
                f"Crowd risk detected: "
                f"{risk_level}"
            ),
            created_at=datetime.now(),
            resolved_at=None,
            status=AlertStatus.ACTIVE
        )

        self.next_alert_id += 1

        self.active_alert = alert

        return {
            "event": "CREATED",
            "alert": alert
        }

    def close(self):
        """
        Resolve an active alert when the
        video/source is stopped or ends.
        """

        if self.active_alert is None:
            return None

        self.active_alert.status = (
            AlertStatus.RESOLVED
        )

        self.active_alert.resolved_at = (
            datetime.now()
        )

        resolved_alert = self.active_alert

        self.active_alert = None

        return {
            "event": "RESOLVED",
            "alert": resolved_alert
        }