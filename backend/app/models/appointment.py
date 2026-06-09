import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Appointment(Base):
    __tablename__ = "appointments"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    patient_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("patients.id"), nullable=False
    )
    practitioner_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("practitioners.id"), nullable=False
    )
    scheduled_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    duration_minutes: Mapped[int] = mapped_column(default=30)
    status: Mapped[str] = mapped_column(
        String(20), default="scheduled",
        comment="scheduled | confirmed | in-progress | completed | cancelled | no-show"
    )
    appointment_type: Mapped[str] = mapped_column(
        String(50), nullable=False,
        comment="e.g. routine-checkup, follow-up, urgent, telehealth"
    )
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    patient: Mapped["Patient"] = relationship(back_populates="appointments")  # noqa: F821
    practitioner: Mapped["Practitioner"] = relationship(  # noqa: F821
        back_populates="appointments"
    )
