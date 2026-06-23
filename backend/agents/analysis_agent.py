from backend.graph.state import IncidentState
from backend.schemas.analysis import RCAReport


async def analysis_agent(state: IncidentState):
    findings = state["research_findings"]

    report = RCAReport(
        root_cause="Database connection pool exhaustion",
        confidence=0.93,
        evidence=[
            findings.metrics_summary,
            findings.log_summary,
            "Similar historical incidents found",
        ],
    )

    return {
        "rca_report": report,
        "resolved": True,
    }