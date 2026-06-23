from pydantic import BaseModel


class ActionPlan(BaseModel):
    severity: str
    actions: list[str]
    requires_approval: bool = True
    proposed_jira_title: str | None = None
    proposed_jira_description: str | None = None
    jira_ticket: dict | None = None