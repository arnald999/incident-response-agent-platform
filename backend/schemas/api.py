from pydantic import BaseModel
from datetime import datetime

from backend.schemas.analysis import RCAReport
from backend.schemas.postmortem import Postmortem
from backend.schemas.research import ResearchFinding
from backend.schemas.response import ActionPlan


class InvestigationRequest(BaseModel):
    alert_details: dict | None = None


class InvestigationSummary(BaseModel):
    incident_id: str
    resolved: bool
    root_cause: str | None = None
    confidence: float | None = None
    created_at: datetime
    updated_at: datetime


class InvestigationListResponse(BaseModel):
    count: int
    investigations: list[InvestigationSummary]


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