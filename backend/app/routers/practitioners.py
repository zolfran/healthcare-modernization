import uuid

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.practitioner import Practitioner
from app.schemas.practitioner import (
    PractitionerCreate,
    PractitionerRead,
    PractitionerUpdate,
)

router = APIRouter(prefix="/practitioners", tags=["Practitioners"])


@router.get("/", response_model=list[PractitionerRead])
def list_practitioners(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    specialty: str | None = None,
    db: Session = Depends(get_db),
) -> list[Practitioner]:
    query = db.query(Practitioner)
    if specialty:
        query = query.filter(Practitioner.specialty.ilike(f"%{specialty}%"))
    return query.order_by(Practitioner.last_name).offset(skip).limit(limit).all()


@router.get("/{practitioner_id}", response_model=PractitionerRead)
def get_practitioner(
    practitioner_id: uuid.UUID, db: Session = Depends(get_db)
) -> Practitioner:
    practitioner = (
        db.query(Practitioner).filter(Practitioner.id == practitioner_id).first()
    )
    if not practitioner:
        raise HTTPException(status_code=404, detail="Practitioner not found")
    return practitioner


@router.post("/", response_model=PractitionerRead, status_code=201)
def create_practitioner(
    body: PractitionerCreate, db: Session = Depends(get_db)
) -> Practitioner:
    existing = db.query(Practitioner).filter(Practitioner.npi == body.npi).first()
    if existing:
        raise HTTPException(status_code=409, detail="NPI already exists")
    practitioner = Practitioner(**body.model_dump())
    db.add(practitioner)
    db.commit()
    db.refresh(practitioner)
    return practitioner


@router.patch("/{practitioner_id}", response_model=PractitionerRead)
def update_practitioner(
    practitioner_id: uuid.UUID,
    body: PractitionerUpdate,
    db: Session = Depends(get_db),
) -> Practitioner:
    practitioner = (
        db.query(Practitioner).filter(Practitioner.id == practitioner_id).first()
    )
    if not practitioner:
        raise HTTPException(status_code=404, detail="Practitioner not found")
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(practitioner, field, value)
    db.commit()
    db.refresh(practitioner)
    return practitioner
