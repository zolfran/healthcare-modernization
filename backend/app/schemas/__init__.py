from app.schemas.appointment import (
    AppointmentCreate,
    AppointmentRead,
    AppointmentUpdate,
)
from app.schemas.observation import ObservationCreate, ObservationRead
from app.schemas.patient import PatientCreate, PatientRead, PatientUpdate
from app.schemas.practitioner import (
    PractitionerCreate,
    PractitionerRead,
    PractitionerUpdate,
)

__all__ = [
    "AppointmentCreate",
    "AppointmentRead",
    "AppointmentUpdate",
    "ObservationCreate",
    "ObservationRead",
    "PatientCreate",
    "PatientRead",
    "PatientUpdate",
    "PractitionerCreate",
    "PractitionerRead",
    "PractitionerUpdate",
]
