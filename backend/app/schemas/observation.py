import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class ObservationBase(BaseModel):
    patient_id: uuid.UUID
    code: str = Field(..., max_length=20)
    display_name: str = Field(..., max_length=100)
    value: float | None = None
    value_string: str | None = None
    unit: str | None = None
    status: str = "final"
    notes: str | None = None


class ObservationCreate(ObservationBase):
    pass


class ObservationRead(ObservationBase):
    id: uuid.UUID
    issued_at: datetime
    created_at: datetime

    model_config = {"from_attributes": True}
