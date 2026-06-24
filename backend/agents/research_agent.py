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

    service_findings = {
        "payments": {
            "metrics": "DB connections at 98%",
            "logs": "Connection timeout errors observed",
        },
        "auth": {
            "metrics": "Authentication failures increased by 400%",
            "logs": "JWT validation service unavailable",
        },
        "messaging": {
            "metrics": "Kafka lag exceeded 250k messages",
            "logs": "Consumer group rebalancing detected",
        },
        "search": {
            "metrics": "P95 latency exceeded 8 seconds",
            "logs": "ElasticSearch query timeouts observed",
        },
        "cache": {
            "metrics": "Redis memory usage reached 95%",
            "logs": "Cache eviction spikes detected",
        },
    }

    findings = service_findings.get(
        incident.service,
        {
            "metrics": "Infrastructure anomaly detected",
            "logs": "No detailed logs available",
        },
    )

    finding = ResearchFinding(
        incident_summary=f"{incident.service} service degradation",
        historical_matches=historical,
        metrics_summary=findings["metrics"],
        log_summary=findings["logs"],
    )

    return {
        "research_findings": finding,
    }