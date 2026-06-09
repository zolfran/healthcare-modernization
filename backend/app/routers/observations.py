import uuid

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.observation import Observation
from app.models.patient import Patient
from app.schemas.observation import ObservationCreate, ObservationRead

router = APIRouter(prefix="/observations", tags=["Observations"])


@router.get("/", response_model=list[ObservationRead])
def list_observations(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    patient_id: uuid.UUID | None = None,
    code: str | None = None,
    db: Session = Depends(get_db),
) -> list[Observation]:
    query = db.query(Observation)
    if patient_id:
        query = query.filter(Observation.patient_id == patient_id)
    if code:
        query = query.filter(Observation.code == code)
    return query.order_by(Observation.issued_at.desc()).offset(skip).limit(limit).all()


@router.get("/{observation_id}", response_model=ObservationRead)
def get_observation(
    observation_id: uuid.UUID, db: Session = Depends(get_db)
) -> Observation:
    obs = db.query(Observation).filter(Observation.id == observation_id).first()
    if not obs:
        raise HTTPException(status_code=404, detail="Observation not found")
    return obs


@router.post("/", response_model=ObservationRead, status_code=201)
def create_observation(
    body: ObservationCreate, db: Session = Depends(get_db)
) -> Observation:
    if not db.query(Patient).filter(Patient.id == body.patient_id).first():
        raise HTTPException(status_code=404, detail="Patient not found")
    obs = Observation(**body.model_dump())
    db.add(obs)
    db.commit()
    db.refresh(obs)
    return obs
