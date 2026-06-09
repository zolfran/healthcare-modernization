"""Seed the database with sample healthcare data."""

import uuid
from datetime import date, datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.database import SessionLocal, engine, Base
from app.models import Appointment, Observation, Patient, Practitioner


def seed() -> None:
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()

    if db.query(Patient).count() > 0:
        print("Database already seeded — skipping.")
        db.close()
        return

    # --- Practitioners ---
    practitioners = [
        Practitioner(
            id=uuid.uuid4(), npi="1234567890", first_name="Sarah",
            last_name="Chen", specialty="Internal Medicine",
            email="sarah.chen@hospital.example", phone="555-0101",
            department="Primary Care",
        ),
        Practitioner(
            id=uuid.uuid4(), npi="2345678901", first_name="James",
            last_name="Wilson", specialty="Cardiology",
            email="james.wilson@hospital.example", phone="555-0102",
            department="Cardiac Care",
        ),
        Practitioner(
            id=uuid.uuid4(), npi="3456789012", first_name="Maria",
            last_name="Garcia", specialty="Pediatrics",
            email="maria.garcia@hospital.example", phone="555-0103",
            department="Pediatrics",
        ),
        Practitioner(
            id=uuid.uuid4(), npi="4567890123", first_name="David",
            last_name="Kim", specialty="Orthopedics",
            email="david.kim@hospital.example", phone="555-0104",
            department="Orthopedics",
        ),
        Practitioner(
            id=uuid.uuid4(), npi="5678901234", first_name="Emily",
            last_name="Taylor", specialty="Dermatology",
            email="emily.taylor@hospital.example", phone="555-0105",
            department="Dermatology",
        ),
    ]
    db.add_all(practitioners)
    db.flush()

    # --- Patients ---
    patients = [
        Patient(
            id=uuid.uuid4(), mrn="MRN-001", first_name="John", last_name="Doe",
            date_of_birth=date(1985, 3, 15), gender="male",
            email="john.doe@example.com", phone="555-1001",
            address_line1="123 Oak Street", city="Springfield", state="IL",
            zip_code="62701", insurance_provider="Blue Cross",
            insurance_id="BC-12345", allergies="Penicillin",
        ),
        Patient(
            id=uuid.uuid4(), mrn="MRN-002", first_name="Jane", last_name="Smith",
            date_of_birth=date(1990, 7, 22), gender="female",
            email="jane.smith@example.com", phone="555-1002",
            address_line1="456 Maple Ave", city="Springfield", state="IL",
            zip_code="62702", insurance_provider="Aetna",
            insurance_id="AE-67890",
        ),
        Patient(
            id=uuid.uuid4(), mrn="MRN-003", first_name="Robert", last_name="Johnson",
            date_of_birth=date(1972, 11, 8), gender="male",
            email="robert.j@example.com", phone="555-1003",
            address_line1="789 Elm Blvd", city="Chicago", state="IL",
            zip_code="60601", insurance_provider="United Health",
            insurance_id="UH-11111", allergies="Sulfa drugs, Latex",
        ),
        Patient(
            id=uuid.uuid4(), mrn="MRN-004", first_name="Maria", last_name="Rodriguez",
            date_of_birth=date(1998, 1, 30), gender="female",
            email="maria.r@example.com", phone="555-1004",
            address_line1="321 Pine Road", city="Chicago", state="IL",
            zip_code="60602", insurance_provider="Cigna",
            insurance_id="CI-22222",
        ),
        Patient(
            id=uuid.uuid4(), mrn="MRN-005", first_name="William", last_name="Brown",
            date_of_birth=date(1965, 5, 12), gender="male",
            email="will.brown@example.com", phone="555-1005",
            address_line1="654 Cedar Lane", city="Naperville", state="IL",
            zip_code="60540", insurance_provider="Medicare",
            insurance_id="MC-33333", allergies="Aspirin",
            notes="History of hypertension",
        ),
        Patient(
            id=uuid.uuid4(), mrn="MRN-006", first_name="Lisa", last_name="Davis",
            date_of_birth=date(2010, 9, 3), gender="female",
            email="lisa.parent@example.com", phone="555-1006",
            address_line1="987 Birch Court", city="Evanston", state="IL",
            zip_code="60201", insurance_provider="Blue Cross",
            insurance_id="BC-44444",
        ),
        Patient(
            id=uuid.uuid4(), mrn="MRN-007", first_name="Michael", last_name="Lee",
            date_of_birth=date(1955, 12, 25), gender="male",
            email="michael.lee@example.com", phone="555-1007",
            address_line1="147 Walnut Street", city="Springfield", state="IL",
            zip_code="62703", insurance_provider="Medicare",
            insurance_id="MC-55555", allergies="NSAIDs",
            notes="Diabetic — Type 2, managed with Metformin",
        ),
        Patient(
            id=uuid.uuid4(), mrn="MRN-008", first_name="Aisha", last_name="Patel",
            date_of_birth=date(1988, 4, 17), gender="female",
            email="aisha.patel@example.com", phone="555-1008",
            address_line1="258 Spruce Drive", city="Peoria", state="IL",
            zip_code="61602", insurance_provider="Aetna",
            insurance_id="AE-66666",
        ),
    ]
    db.add_all(patients)
    db.flush()

    # --- Appointments ---
    now = datetime.now(timezone.utc)
    appointments = [
        Appointment(
            patient_id=patients[0].id, practitioner_id=practitioners[0].id,
            scheduled_at=now + timedelta(days=2, hours=9),
            appointment_type="routine-checkup", status="scheduled",
            reason="Annual physical",
        ),
        Appointment(
            patient_id=patients[0].id, practitioner_id=practitioners[1].id,
            scheduled_at=now + timedelta(days=5, hours=14),
            appointment_type="follow-up", status="scheduled",
            reason="Cardiac follow-up after stress test",
        ),
        Appointment(
            patient_id=patients[1].id, practitioner_id=practitioners[0].id,
            scheduled_at=now + timedelta(days=1, hours=10),
            appointment_type="urgent", status="confirmed",
            reason="Persistent headaches",
        ),
        Appointment(
            patient_id=patients[2].id, practitioner_id=practitioners[3].id,
            scheduled_at=now - timedelta(days=3, hours=11),
            appointment_type="follow-up", status="completed",
            reason="Post-surgery knee evaluation",
            notes="Recovery progressing well, cleared for light exercise",
        ),
        Appointment(
            patient_id=patients[3].id, practitioner_id=practitioners[4].id,
            scheduled_at=now + timedelta(days=7, hours=15),
            appointment_type="routine-checkup", status="scheduled",
            reason="Skin assessment",
        ),
        Appointment(
            patient_id=patients[4].id, practitioner_id=practitioners[1].id,
            scheduled_at=now - timedelta(days=1, hours=8),
            appointment_type="urgent", status="completed",
            reason="Chest discomfort and shortness of breath",
            notes="EKG normal, stress test ordered",
        ),
        Appointment(
            patient_id=patients[5].id, practitioner_id=practitioners[2].id,
            scheduled_at=now + timedelta(days=3, hours=13),
            appointment_type="routine-checkup", status="scheduled",
            reason="Annual pediatric wellness visit",
        ),
        Appointment(
            patient_id=patients[6].id, practitioner_id=practitioners[0].id,
            scheduled_at=now + timedelta(days=1, hours=11),
            appointment_type="follow-up", status="confirmed",
            reason="Diabetes management review",
        ),
        Appointment(
            patient_id=patients[7].id, practitioner_id=practitioners[0].id,
            scheduled_at=now - timedelta(days=7, hours=9),
            appointment_type="telehealth", status="completed",
            reason="General wellness check",
        ),
    ]
    db.add_all(appointments)

    # --- Observations (vitals / lab results) ---
    observations = [
        # John Doe vitals
        Observation(
            patient_id=patients[0].id, code="8867-4",
            display_name="Heart Rate", value=72, unit="bpm",
        ),
        Observation(
            patient_id=patients[0].id, code="8480-6",
            display_name="Systolic Blood Pressure", value=128, unit="mmHg",
        ),
        Observation(
            patient_id=patients[0].id, code="8462-4",
            display_name="Diastolic Blood Pressure", value=82, unit="mmHg",
        ),
        Observation(
            patient_id=patients[0].id, code="8310-5",
            display_name="Body Temperature", value=98.6, unit="°F",
        ),
        # Jane Smith vitals
        Observation(
            patient_id=patients[1].id, code="8867-4",
            display_name="Heart Rate", value=68, unit="bpm",
        ),
        Observation(
            patient_id=patients[1].id, code="8480-6",
            display_name="Systolic Blood Pressure", value=118, unit="mmHg",
        ),
        # William Brown — hypertensive
        Observation(
            patient_id=patients[4].id, code="8867-4",
            display_name="Heart Rate", value=88, unit="bpm",
        ),
        Observation(
            patient_id=patients[4].id, code="8480-6",
            display_name="Systolic Blood Pressure", value=155, unit="mmHg",
        ),
        Observation(
            patient_id=patients[4].id, code="8462-4",
            display_name="Diastolic Blood Pressure", value=95, unit="mmHg",
        ),
        Observation(
            patient_id=patients[4].id, code="2339-0",
            display_name="Glucose", value=142, unit="mg/dL",
            notes="Fasting glucose — slightly elevated",
        ),
        # Michael Lee — diabetic
        Observation(
            patient_id=patients[6].id, code="4548-4",
            display_name="Hemoglobin A1c", value=7.2, unit="%",
            notes="Target < 7.0%",
        ),
        Observation(
            patient_id=patients[6].id, code="2339-0",
            display_name="Glucose", value=168, unit="mg/dL",
        ),
        Observation(
            patient_id=patients[6].id, code="8480-6",
            display_name="Systolic Blood Pressure", value=140, unit="mmHg",
        ),
        # Lisa Davis — pediatric
        Observation(
            patient_id=patients[5].id, code="8867-4",
            display_name="Heart Rate", value=90, unit="bpm",
        ),
        Observation(
            patient_id=patients[5].id, code="8310-5",
            display_name="Body Temperature", value=98.4, unit="°F",
        ),
    ]
    db.add_all(observations)

    db.commit()
    db.close()
    print(f"Seeded {len(patients)} patients, {len(practitioners)} practitioners, "
          f"{len(appointments)} appointments, {len(observations)} observations.")


if __name__ == "__main__":
    seed()
