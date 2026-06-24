from typing import Any

from fastmcp import Client

from backend.core.config import settings
from backend.schemas.incident import Incident


class MCPClient:
    async def _call_tool(
        self,
        tool_name: str,
        arguments: dict[str, Any] | None = None,
    ):
        if not settings.use_real_mcp or not settings.mcp_server_url:
            raise RuntimeError("Real MCP is disabled.")

        client = Client(settings.mcp_server_url)

        async with client:
            result = await client.call_tool(
                tool_name,
                arguments or {},
            )

        return result.data

    async def get_incident(
        self,
        incident_id: str,
    ) -> Incident:
        try:
            data = await self._call_tool(
                "get_incident",
                {"incident_id": incident_id},
            )

            return Incident(
                id=data.get("id", incident_id),
                title=data.get("title", "Unknown incident"),
                severity=data.get("severity", "medium"),
                service=data.get("service", "unknown"),
            )

        except Exception:
            return self._mock_incident(incident_id)

    async def search_incidents(
        self,
        query: str,
    ):
        try:
            data = await self._call_tool(
                "search_incidents",
                {"query": query},
            )

            if isinstance(data, list):
                return [
                    item.get("id", str(item))
                    if isinstance(item, dict)
                    else str(item)
                    for item in data
                ]

            return []

        except Exception:
            return ["INC-420", "INC-300"]

    async def create_jira_ticket(
        self,
        title: str,
        description: str,
    ):
        try:
            data = await self._call_tool(
                "create_jira_ticket",
                {
                    "title": title,
                    "description": description,
                },
            )

            return data

        except Exception:
            return {
                "ticket_id": "JIRA-MOCK-100",
                "status": "created",
                "title": title,
                "description": description,
            }

    def _mock_incident(
        self,
        incident_id: str,
    ) -> Incident:
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