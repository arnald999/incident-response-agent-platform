from pydantic import BaseModel


class ResearchFinding(BaseModel):
    incident_summary: str
    historical_matches: list[str]
    metrics_summary: str
    log_summary: str