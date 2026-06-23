from pydantic import BaseModel


class Postmortem(BaseModel):
    summary: str
    timeline: list[str]
    lessons_learned: list[str]