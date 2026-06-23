from sqlalchemy import select

from backend.db import AsyncSessionLocal
from backend.models.investigation import Investigation


def to_dict(value):
    if hasattr(value, "model_dump"):
        return value.model_dump()
    return value


class InvestigationRepository:

    async def save(self, data: dict) -> Investigation:
        async with AsyncSessionLocal() as session:
            existing = await session.get(Investigation, data["incident_id"])

            payload = {
                "incident_id": data["incident_id"],
                "resolved": data["resolved"],
                "research_findings": to_dict(data["research_findings"]),
                "rca_report": to_dict(data["rca_report"]),
                "action_plan": to_dict(data["action_plan"]),
                "postmortem": to_dict(data["postmortem"]),
            }

            if existing:
                for key, value in payload.items():
                    setattr(existing, key, value)
                record = existing
            else:
                record = Investigation(**payload)
                session.add(record)

            await session.commit()
            await session.refresh(record)
            return record

    async def list_all(self) -> list[Investigation]:
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(Investigation))
            return list(result.scalars().all())

    async def get_by_incident_id(self, incident_id: str) -> Investigation | None:
        async with AsyncSessionLocal() as session:
            return await session.get(Investigation, incident_id)