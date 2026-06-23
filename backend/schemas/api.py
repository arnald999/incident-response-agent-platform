from pydantic import BaseModel

from backend.schemas.analysis import RCAReport
from backend.schemas.postmortem import Postmortem
from backend.schemas.research import ResearchFinding
from backend.schemas.response import ActionPlan


class InvestigationRequest(BaseModel):
    alert_details: dict | None = None


class InvestigationListResponse(BaseModel):
    count: int
    incident_ids: list[str]


class InvestigationResponse(BaseModel):
    incident_id: str
    research_findings: ResearchFinding
    rca_report: RCAReport
    action_plan: ActionPlan
    postmortem: Postmortem
    resolved: bool


class JiraApprovalResponse(BaseModel):
    incident_id: str
    jira_ticket: dict
    status: str