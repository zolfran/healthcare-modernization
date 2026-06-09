import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class AppointmentBase(BaseModel):
    patient_id: uuid.UUID
    practitioner_id: uuid.UUID
    scheduled_at: datetime
    duration_minutes: int = 30
    appointment_type: str = Field(..., max_length=50)
    reason: str | None = None
    notes: str | None = None


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentUpdate(BaseModel):
    scheduled_at: datetime | None = None
    duration_minutes: int | None = None
    status: str | None = None
    appointment_type: str | None = None
    reason: str | None = None
    notes: str | None = None


class AppointmentRead(AppointmentBase):
    id: uuid.UUID
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
