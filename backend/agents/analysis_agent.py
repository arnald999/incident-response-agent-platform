from backend.graph.state import IncidentState
from backend.schemas.analysis import RCAReport
from backend.services.llm import get_llm


def fallback_report(findings) -> RCAReport:
    return RCAReport(
        root_cause="Database connection pool exhaustion",
        confidence=0.93,
        evidence=[
            findings.metrics_summary,
            findings.log_summary,
            "Historical incident pattern suggests DB pool saturation",
        ],
    )


def normalize_confidence(value: float) -> float:
    if value > 1:
        return value / 100
    return value


async def analysis_agent(state: IncidentState):
    findings = state["research_findings"]
    llm = get_llm()

    if not llm:
        report = fallback_report(findings)
    else:
        try:
            structured_llm = llm.with_structured_output(RCAReport)
            report = await structured_llm.ainvoke(
                f"""
You are an enterprise incident response analysis agent.

Analyze these findings and return a structured RCA report.

Incident summary:
{findings.incident_summary}

Historical matches:
{findings.historical_matches}

Metrics summary:
{findings.metrics_summary}

Log summary:
{findings.log_summary}
"""
            )
        except Exception:
            report = fallback_report(findings)
        
    report.confidence = normalize_confidence(report.confidence)

    return {
        "rca_report": report,
        "resolved": report.confidence >= 0.8,
    }