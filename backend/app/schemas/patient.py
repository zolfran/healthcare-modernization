import uuid
from datetime import date, datetime

from pydantic import BaseModel, Field


class PatientBase(BaseModel):
    first_name: str = Field(..., max_length=100)
    last_name: str = Field(..., max_length=100)
    date_of_birth: date
    gender: str = Field(..., max_length=20)
    email: str | None = Field(None, max_length=255)
    phone: str | None = Field(None, max_length=20)
    address_line1: str | None = None
    address_line2: str | None = None
    city: str | None = None
    state: str | None = None
    zip_code: str | None = None
    insurance_provider: str | None = None
    insurance_id: str | None = None
    allergies: str | None = None
    notes: str | None = None


class PatientCreate(PatientBase):
    mrn: str = Field(..., max_length=20)


class PatientUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    phone: str | None = None
    address_line1: str | None = None
    address_line2: str | None = None
    city: str | None = None
    state: str | None = None
    zip_code: str | None = None
    insurance_provider: str | None = None
    insurance_id: str | None = None
    allergies: str | None = None
    notes: str | None = None
    active: bool | None = None


class PatientRead(PatientBase):
    id: uuid.UUID
    mrn: str
    active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
