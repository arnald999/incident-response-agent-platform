from backend.graph.state import IncidentState
from backend.schemas.postmortem import Postmortem


async def postmortem_agent(state: IncidentState):
    rca = state["rca_report"]
    action_plan = state["action_plan"]

    postmortem = Postmortem(
        summary=f"Incident caused by {rca.root_cause}.",
        timeline=[
            "Alert triggered",
            "Research agent gathered incident context",
            "Analysis agent identified probable root cause",
            "Response agent generated remediation plan",
        ],
        lessons_learned=[
            "Alert earlier on DB connection pressure",
            "Review autoscaling and database pool limits",
            "Use historical incidents to speed up investigation",
        ],
    )

    return {
        "postmortem": postmortem,
    }