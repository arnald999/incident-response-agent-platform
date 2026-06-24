from backend.schemas.incident import Incident


class MCPClient:

    from backend.schemas.incident import Incident


class MCPClient:

    async def get_incident(self, incident_id: str) -> Incident:

        incidents = {
            "INC-500": Incident(
                id="INC-500",
                title="Payment API latency spike",
                severity="critical",
                service="payments",
            ),
            "INC-501": Incident(
                id="INC-501",
                title="Authentication service outage",
                severity="critical",
                service="auth",
            ),
            "INC-502": Incident(
                id="INC-502",
                title="Kafka consumer lag increase",
                severity="high",
                service="messaging",
            ),
            "INC-503": Incident(
                id="INC-503",
                title="Search API timeout errors",
                severity="high",
                service="search",
            ),
            "INC-504": Incident(
                id="INC-504",
                title="Redis cache saturation",
                severity="medium",
                service="cache",
            ),
        }

        return incidents.get(
            incident_id,
            Incident(
                id=incident_id,
                title="Unknown Incident",
                severity="medium",
                service="unknown",
            ),
        )

    async def search_incidents(self, query: str):
        return ["INC-420", "INC-300"]

    async def create_jira_ticket(self, title: str, description: str):
        return {
            "ticket_id": "JIRA-100",
            "status": "created",
            "title": title,
            "description": description,
        }