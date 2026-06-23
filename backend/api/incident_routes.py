from fastapi import APIRouter, HTTPException

from backend.graph.workflow import incident_workflow
from backend.schemas.api import InvestigationResponse, JiraApprovalResponse
from backend.tools.mcp_client import MCPClient

router = APIRouter(prefix="/incidents", tags=["Incidents"])
mcp = MCPClient()

LATEST_RESULTS = {}


@router.post(
    "/{incident_id}/investigate",
    response_model=InvestigationResponse,
)
async def investigate_incident(incident_id: str):
    result = await incident_workflow.ainvoke({"incident_id": incident_id})
    LATEST_RESULTS[incident_id] = result
    return result


@router.post(
    "/{incident_id}/approve-jira",
    response_model=JiraApprovalResponse,
)
async def approve_jira(incident_id: str):
    result = LATEST_RESULTS.get(incident_id)

    if not result:
        raise HTTPException(
            status_code=404,
            detail="No investigation found for this incident.",
        )

    action_plan = result["action_plan"]

    ticket = await mcp.create_jira_ticket(
        title=action_plan.proposed_jira_title or "Incident remediation",
        description=action_plan.proposed_jira_description or "",
    )

    action_plan.jira_ticket = ticket
    action_plan.requires_approval = False

    return {
        "incident_id": incident_id,
        "jira_ticket": ticket,
        "status": "approved",
    }