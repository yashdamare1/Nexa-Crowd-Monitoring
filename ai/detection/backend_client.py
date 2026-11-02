import os
import requests
import uuid


class NexaBackendClient:
    def __init__(self, base_url=None):
        self.base_url = (
            base_url or
            os.getenv("NEXA_API_URL", "http://localhost:8081")
        ).rstrip("/")

        self.session = requests.Session()
        self.token = None
        self.pipeline_run_id = str(uuid.uuid4())

    def login(self, email=None, password=None):
        email = email or os.getenv("NEXA_EMAIL")
        password = password or os.getenv("NEXA_PASSWORD")

        if not email or not password:
            raise ValueError(
                "Set NEXA_EMAIL and NEXA_PASSWORD environment variables."
            )

        response = self.session.post(
            f"{self.base_url}/api/auth/login",
            json={
                "email": email,
                "password": password
            },
            timeout=10
        )
        response.raise_for_status()

        data = response.json()
        self.token = data.get("token")

        if not self.token:
            raise RuntimeError(
                "Login response did not contain a JWT token."
            )

        print("Nexa backend login successful.")
        print(f"Pipeline Run ID: {self.pipeline_run_id}")

        return True

    def _auth_headers(self):
        if not self.token:
            raise RuntimeError(
                "Not authenticated. Call login() first."
            )

        return {
            "Authorization": f"Bearer {self.token}"
        }

    def send_monitoring_update(
        self,
        source_id,
        person_count,
        risk_level,
        source_online=True
    ):
        response = self.session.post(
            f"{self.base_url}/api/security/monitoring/updates",
            headers=self._auth_headers(),
            json={
                "sourceId": source_id,
                "personCount": int(person_count),
                "riskLevel": str(risk_level).upper(),
                "sourceOnline": bool(source_online)
            },
            timeout=5
        )

        response.raise_for_status()
        return response.json()

    def send_alert_event(self, source_id, alert, event_type):
        event_type = str(event_type).upper()

        if event_type not in {
            "CREATED",
            "ESCALATED",
            "RESOLVED"
        }:
            raise ValueError(
                f"Unsupported alert event: {event_type}"
            )

        status = str(alert.status.value).upper()

        payload = {
            "sourceAlertId": int(alert.alert_id),
            "pipelineRunId": self.pipeline_run_id,
            "sourceId": source_id,
            "eventType": event_type,
            "riskLevel": str(alert.risk_level).upper(),
            "message": str(alert.message),
            "status": status,
            "createdAt": alert.created_at.isoformat(),
            "resolvedAt": (
                alert.resolved_at.isoformat()
                if alert.resolved_at else None
            )
        }

        response = self.session.post(
            f"{self.base_url}/api/security/alerts",
            headers=self._auth_headers(),
            json=payload,
            timeout=5
        )

        response.raise_for_status()
        return response.json()