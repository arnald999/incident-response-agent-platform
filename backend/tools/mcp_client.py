from backend.schemas.incident import Incident


class MCPClient:

    async def get_incident(self, incident_id: str) -> Incident:
        return Incident(
            id=incident_id,
            title="Payment API latency spike",
            severity="critical",
            service="payments",
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