from backend.graph.state import IncidentState
from backend.schemas.response import ActionPlan


async def response_agent(state: IncidentState):
    rca = state["rca_report"]

    actions = [
        "Restart affected payment API pods",
        "Increase database connection pool size",
        "Add alert for DB connection usage above 85%",
    ]

    plan = ActionPlan(
        severity="critical",
        actions=actions,
        requires_approval=True,
        proposed_jira_title=f"Remediation required: {rca.root_cause}",
        proposed_jira_description=(
            f"Root cause: {rca.root_cause}\n\n"
            f"Confidence: {rca.confidence}\n\n"
            f"Evidence:\n- " + "\n- ".join(rca.evidence) + "\n\n"
            f"Recommended actions:\n- " + "\n- ".join(actions)
        ),
    )

    return {"action_plan": plan}