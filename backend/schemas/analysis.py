from pydantic import BaseModel


class RCAReport(BaseModel):
    root_cause: str
    confidence: float
    evidence: list[str]