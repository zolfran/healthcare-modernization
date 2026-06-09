import uuid

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.appointment import Appointment
from app.models.patient import Patient
from app.models.practitioner import Practitioner
from app.schemas.appointment import (
    AppointmentCreate,
    AppointmentRead,
    AppointmentUpdate,
)

router = APIRouter(prefix="/appointments", tags=["Appointments"])

VALID_STATUSES = {
    "scheduled", "confirmed", "in-progress", "completed", "cancelled", "no-show"
}


@router.get("/", response_model=list[AppointmentRead])
def list_appointments(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    patient_id: uuid.UUID | None = None,
    practitioner_id: uuid.UUID | None = None,
    status: str | None = None,
    db: Session = Depends(get_db),
) -> list[Appointment]:
    query = db.query(Appointment)
    if patient_id:
        query = query.filter(Appointment.patient_id == patient_id)
    if practitioner_id:
        query = query.filter(Appointment.practitioner_id == practitioner_id)
    if status:
        query = query.filter(Appointment.status == status)
    return query.order_by(Appointment.scheduled_at.desc()).offset(skip).limit(limit).all()


@router.get("/{appointment_id}", response_model=AppointmentRead)
def get_appointment(
    appointment_id: uuid.UUID, db: Session = Depends(get_db)
) -> Appointment:
    appt = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appt


@router.post("/", response_model=AppointmentRead, status_code=201)
def create_appointment(
    body: AppointmentCreate, db: Session = Depends(get_db)
) -> Appointment:
    if not db.query(Patient).filter(Patient.id == body.patient_id).first():
        raise HTTPException(status_code=404, detail="Patient not found")
    if not db.query(Practitioner).filter(Practitioner.id == body.practitioner_id).first():
        raise HTTPException(status_code=404, detail="Practitioner not found")
    appt = Appointment(**body.model_dump())
    db.add(appt)
    db.commit()
    db.refresh(appt)
    return appt


@router.patch("/{appointment_id}", response_model=AppointmentRead)
def update_appointment(
    appointment_id: uuid.UUID,
    body: AppointmentUpdate,
    db: Session = Depends(get_db),
) -> Appointment:
    appt = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    updates = body.model_dump(exclude_unset=True)
    if "status" in updates and updates["status"] not in VALID_STATUSES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status. Must be one of: {', '.join(sorted(VALID_STATUSES))}",
        )
    for field, value in updates.items():
        setattr(appt, field, value)
    db.commit()
    db.refresh(appt)
    return appt
