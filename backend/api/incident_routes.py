from fastapi import APIRouter, HTTPException

from backend.graph.workflow import incident_workflow
from backend.repositories.investigation_repository import InvestigationRepository
from backend.schemas.api import InvestigationRequest, InvestigationResponse, JiraApprovalResponse
from backend.tools.mcp_client import MCPClient

router = APIRouter(prefix="/incidents", tags=["Incidents"])

mcp = MCPClient()
repo = InvestigationRepository()


@router.post(
    "/{incident_id}/investigate",
    response_model=InvestigationResponse,
)
async def investigate_incident(
    incident_id: str,
    request: InvestigationRequest | None = None,
):
    initial_state = {
        "incident_id": incident_id,
        "alert_details": request.alert_details if request else {},
    }

    result = await incident_workflow.ainvoke(initial_state)
    await repo.save(result)

    return result


@router.get("")
async def list_investigations():
    records = await repo.list_all()

    return {
        "count": len(records),
        "incident_ids": [record.incident_id for record in records],
    }


@router.post(
    "/{incident_id}/approve-jira",
    response_model=JiraApprovalResponse,
)
async def approve_jira(incident_id: str):
    record = await repo.get_by_incident_id(incident_id)

    if not record:
        raise HTTPException(
            status_code=404,
            detail="No investigation found for this incident.",
        )

    action_plan = record.action_plan

    ticket = await mcp.create_jira_ticket(
        title=action_plan.get("proposed_jira_title") or "Incident remediation",
        description=action_plan.get("proposed_jira_description") or "",
    )

    action_plan["jira_ticket"] = ticket
    action_plan["requires_approval"] = False

    record.action_plan = action_plan

    await repo.save(
        {
            "incident_id": record.incident_id,
            "resolved": record.resolved,
            "research_findings": record.research_findings,
            "rca_report": record.rca_report,
            "action_plan": record.action_plan,
            "postmortem": record.postmortem,
        }
    )

    return {
        "incident_id": incident_id,
        "jira_ticket": ticket,
        "status": "approved",
    }