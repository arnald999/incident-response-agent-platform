from typing import TypedDict

from backend.schemas.research import ResearchFinding
from backend.schemas.analysis import RCAReport
from backend.schemas.response import ActionPlan
from backend.schemas.postmortem import Postmortem


class IncidentState(TypedDict, total=False):
    incident_id: str

    research_findings: ResearchFinding
    rca_report: RCAReport
    action_plan: ActionPlan
    postmortem: Postmortem

    resolved: bool