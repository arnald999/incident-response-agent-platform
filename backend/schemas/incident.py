from pydantic import BaseModel


class Incident(BaseModel):
    id: str
    title: str
    severity: str
    service: str