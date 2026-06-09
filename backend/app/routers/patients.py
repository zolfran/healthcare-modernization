import uuid

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.patient import Patient
from app.schemas.patient import PatientCreate, PatientRead, PatientUpdate

router = APIRouter(prefix="/patients", tags=["Patients"])


@router.get("/", response_model=list[PatientRead])
def list_patients(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    active: bool | None = None,
    search: str | None = None,
    db: Session = Depends(get_db),
) -> list[Patient]:
    query = db.query(Patient)
    if active is not None:
        query = query.filter(Patient.active == active)
    if search:
        pattern = f"%{search}%"
        query = query.filter(
            Patient.first_name.ilike(pattern)
            | Patient.last_name.ilike(pattern)
            | Patient.mrn.ilike(pattern)
        )
    return query.order_by(Patient.last_name).offset(skip).limit(limit).all()


@router.get("/{patient_id}", response_model=PatientRead)
def get_patient(patient_id: uuid.UUID, db: Session = Depends(get_db)) -> Patient:
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


@router.post("/", response_model=PatientRead, status_code=201)
def create_patient(body: PatientCreate, db: Session = Depends(get_db)) -> Patient:
    existing = db.query(Patient).filter(Patient.mrn == body.mrn).first()
    if existing:
        raise HTTPException(status_code=409, detail="MRN already exists")
    patient = Patient(**body.model_dump())
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient


@router.patch("/{patient_id}", response_model=PatientRead)
def update_patient(
    patient_id: uuid.UUID, body: PatientUpdate, db: Session = Depends(get_db)
) -> Patient:
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(patient, field, value)
    db.commit()
    db.refresh(patient)
    return patient


@router.delete("/{patient_id}", status_code=204)
def delete_patient(patient_id: uuid.UUID, db: Session = Depends(get_db)) -> None:
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    db.delete(patient)
    db.commit()
