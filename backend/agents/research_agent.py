from backend.graph.state import IncidentState
from backend.schemas.research import ResearchFinding
from backend.tools.mcp_client import MCPClient


mcp = MCPClient()


async def research_agent(
    state: IncidentState,
):
    incident = await mcp.get_incident(
        state["incident_id"]
    )

    historical = await mcp.search_incidents(
        incident.service
    )

    finding = ResearchFinding(
        incident_summary=f"{incident.service} service degradation",
        historical_matches=historical,
        metrics_summary="DB connections 98%",
        log_summary="Connection timeout errors observed",
    )

    return {
        "research_findings": finding,
    }