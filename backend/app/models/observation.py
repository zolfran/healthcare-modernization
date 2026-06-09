import uuid
from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Observation(Base):
    """FHIR-inspired clinical observation (vitals, lab results, etc.)."""

    __tablename__ = "observations"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    patient_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("patients.id"), nullable=False
    )
    code: Mapped[str] = mapped_column(
        String(20), nullable=False,
        comment="LOINC-style code, e.g. 8867-4 (heart rate)"
    )
    display_name: Mapped[str] = mapped_column(String(100), nullable=False)
    value: Mapped[float | None] = mapped_column(Float, nullable=True)
    value_string: Mapped[str | None] = mapped_column(String(255), nullable=True)
    unit: Mapped[str | None] = mapped_column(String(20), nullable=True)
    status: Mapped[str] = mapped_column(
        String(20), default="final",
        comment="registered | preliminary | final | amended | cancelled"
    )
    issued_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    patient: Mapped["Patient"] = relationship(back_populates="observations")  # noqa: F821
