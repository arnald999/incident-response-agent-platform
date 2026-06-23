from datetime import datetime

from sqlalchemy import DateTime, String, Boolean, JSON
from sqlalchemy.orm import Mapped, mapped_column

from backend.db import Base


class Investigation(Base):
    __tablename__ = "investigations"

    incident_id: Mapped[str] = mapped_column(String, primary_key=True)
    resolved: Mapped[bool] = mapped_column(Boolean, default=False)

    research_findings: Mapped[dict] = mapped_column(JSON)
    rca_report: Mapped[dict] = mapped_column(JSON)
    action_plan: Mapped[dict] = mapped_column(JSON)
    postmortem: Mapped[dict] = mapped_column(JSON)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )