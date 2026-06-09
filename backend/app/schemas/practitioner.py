import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class PractitionerBase(BaseModel):
    first_name: str = Field(..., max_length=100)
    last_name: str = Field(..., max_length=100)
    specialty: str = Field(..., max_length=100)
    email: str | None = None
    phone: str | None = None
    department: str | None = None


class PractitionerCreate(PractitionerBase):
    npi: str = Field(..., max_length=10)


class PractitionerUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    specialty: str | None = None
    email: str | None = None
    phone: str | None = None
    department: str | None = None
    active: bool | None = None


class PractitionerRead(PractitionerBase):
    id: uuid.UUID
    npi: str
    active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
