from backend.graph.state import IncidentState
from backend.schemas.response import ActionPlan


def build_actions(root_cause: str) -> list[str]:
    text = root_cause.lower()

    if "database" in text or "connection pool" in text:
        return [
            "Restart affected service pods",
            "Increase database connection pool size",
            "Add alert for DB connection usage above 85%",
        ]

    if "authentication" in text or "jwt" in text:
        return [
            "Check authentication service health",
            "Validate JWT signing/verification dependencies",
            "Fail over to backup auth service if available",
        ]

    if "kafka" in text or "consumer" in text or "lag" in text:
        return [
            "Scale affected Kafka consumer group",
            "Check broker health and partition imbalance",
            "Review recent deploys affecting message processing",
        ]

    if "redis" in text or "cache" in text:
        return [
            "Check Redis memory pressure",
            "Increase cache capacity or eviction thresholds",
            "Review hot keys and cache usage patterns",
        ]

    return [
        "Escalate to on-call engineer for triage",
        "Collect additional logs, metrics, and traces",
        "Create follow-up ticket for deeper investigation",
    ]


async def response_agent(state: IncidentState):
    rca = state["rca_report"]

    actions = build_actions(rca.root_cause)

    plan = ActionPlan(
        severity="critical",
        actions=actions,
        requires_approval=True,
        proposed_jira_title=f"Remediation required: {rca.root_cause[:120]}",
        proposed_jira_description=(
            f"Root cause: {rca.root_cause}\n\n"
            f"Confidence: {rca.confidence}\n\n"
            f"Evidence:\n- " + "\n- ".join(rca.evidence) + "\n\n"
            f"Recommended actions:\n- " + "\n- ".join(actions)
        ),
    )

    return {"action_plan": plan}