from fastapi import APIRouter, HTTPException

from backend.graph.workflow import incident_workflow
from backend.repositories.investigation_repository import InvestigationRepository
from backend.schemas.api import (
    InvestigationListResponse,
    InvestigationRequest,
    InvestigationResponse,
    JiraApprovalResponse,
)
from backend.tools.mcp_client import MCPClient
from backend.observability.langfuse import get_langfuse_handler

router = APIRouter(prefix="/incidents", tags=["Incidents"])

mcp = MCPClient()
repo = InvestigationRepository()



@router.get(
    "",
    response_model=InvestigationListResponse,
)
async def list_investigations():
    records = await repo.list_all()

    return {
        "count": len(records),
        "investigations": [
            {
                "incident_id": record.incident_id,
                "resolved": record.resolved,
                "root_cause": record.rca_report.get("root_cause"),
                "confidence": record.rca_report.get("confidence"),
                "created_at": record.created_at,
                "updated_at": record.updated_at,
            }
            for record in records
        ],
    }


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

    handler = get_langfuse_handler()
    callbacks = [handler] if handler else []

    result = await incident_workflow.ainvoke(
        initial_state,
        config={
            "callbacks": callbacks,
            "metadata": {
                "project": "incident-response-agent-platform",
                "incident_id": incident_id,
                "workflow": "incident_investigation",
            },
            "tags": [
                "incident-response-agent-platform",
                "langgraph",
                "fde-roadmap",
            ],
            "run_name": f"incident-investigation-{incident_id}",
        },
    )
    return result


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

@router.get(
    "/{incident_id}",
    response_model=InvestigationResponse,
)
async def get_investigation(incident_id: str):
    record = await repo.get_by_incident_id(incident_id)

    if not record:
        raise HTTPException(
            status_code=404,
            detail="Investigation not found.",
        )

    return {
        "incident_id": record.incident_id,
        "research_findings": record.research_findings,
        "rca_report": record.rca_report,
        "action_plan": record.action_plan,
        "postmortem": record.postmortem,
        "resolved": record.resolved,
    }