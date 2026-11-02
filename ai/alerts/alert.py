from dataclasses import dataclass
from datetime import datetime

from alert_status import AlertStatus


@dataclass
class Alert:
    """
    Represents a crowd-risk alert.
    """

    alert_id: int
    risk_level: str
    message: str
    created_at: datetime
    resolved_at: datetime | None
    status: AlertStatus