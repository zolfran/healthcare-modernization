# HealthHub — Healthcare Modernization Platform

A full-stack reference application demonstrating the modernization of healthcare systems. Built with **FastAPI**, **React + TypeScript**, **PostgreSQL**, and **Docker**, this project showcases patterns commonly found in healthcare IT modernization initiatives including FHIR-inspired data models, RESTful APIs, and a modern responsive UI.

---

## Architecture

```
┌─────────────────────┐     ┌──────────────────────────┐     ┌──────────────┐
│  React + TypeScript  │────▶│  FastAPI (Python 3.12)   │────▶│  PostgreSQL  │
│  Vite + TailwindCSS  │     │  /api/v1/*               │     │  16-alpine   │
│  Port 5173 (dev)     │     │  Port 8000               │     │  Port 5432   │
└─────────────────────┘     └──────────────────────────┘     └──────────────┘
```

## Features

- **Patient Management** — full CRUD for patient records with MRN, demographics, insurance, and allergy tracking
- **Practitioner Directory** — provider registry with NPI, specialty, and department info
- **Appointment Scheduling** — create, update, and filter appointments with status tracking (scheduled → confirmed → in-progress → completed)
- **Clinical Observations** — FHIR-inspired vitals and lab results using LOINC-style codes
- **Dashboard** — at-a-glance stats, recent patients, and upcoming appointments
- **Search** — real-time patient search by name or MRN
- **Seed Data** — pre-populated demo data for 8 patients, 5 practitioners, 9 appointments, and 15 clinical observations

## Tech Stack

| Layer      | Technology                        |
| ---------- | --------------------------------- |
| Frontend   | React 18, TypeScript, Vite, TailwindCSS, React Router, Lucide Icons |
| Backend    | Python 3.12, FastAPI, SQLAlchemy 2.0, Pydantic v2 |
| Database   | PostgreSQL 16                     |
| Infra      | Docker, Docker Compose            |

## Quick Start

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) & Docker Compose
- (Optional) Node.js 20+ and Python 3.12+ for local dev without Docker

### Run with Docker Compose

```bash
# Clone the repo
git clone https://github.com/zolfran/healthcare-modernization.git
cd healthcare-modernization

# Start all services
docker compose up --build

# Seed the database (in a separate terminal)
docker compose exec backend python -m app.seed
```

- **Frontend**: http://localhost:3000
- **API Docs (Swagger)**: http://localhost:8000/docs
- **API Docs (ReDoc)**: http://localhost:8000/redoc

### Run Locally (Development)

#### Backend

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Start PostgreSQL (or set HEALTHCARE_DATABASE_URL)
export HEALTHCARE_DATABASE_URL=postgresql://healthcare:healthcare@localhost:5432/healthcare

uvicorn app.main:app --reload --port 8000

# Seed sample data
python -m app.seed
```

#### Frontend

```bash
cd frontend
npm install
npm run dev
# Open http://localhost:5173
```

The Vite dev server proxies `/api` requests to the backend at `localhost:8000`.

## API Reference

All endpoints are under `/api/v1`. Interactive docs available at `/docs`.

| Method   | Endpoint                          | Description                 |
| -------- | --------------------------------- | --------------------------- |
| `GET`    | `/api/health`                     | Health check                |
| `GET`    | `/api/v1/patients/`               | List patients               |
| `POST`   | `/api/v1/patients/`               | Create patient              |
| `GET`    | `/api/v1/patients/{id}`           | Get patient                 |
| `PATCH`  | `/api/v1/patients/{id}`           | Update patient              |
| `DELETE` | `/api/v1/patients/{id}`           | Delete patient              |
| `GET`    | `/api/v1/practitioners/`          | List practitioners          |
| `POST`   | `/api/v1/practitioners/`          | Create practitioner         |
| `GET`    | `/api/v1/practitioners/{id}`      | Get practitioner            |
| `PATCH`  | `/api/v1/practitioners/{id}`      | Update practitioner         |
| `GET`    | `/api/v1/appointments/`           | List appointments           |
| `POST`   | `/api/v1/appointments/`           | Create appointment          |
| `GET`    | `/api/v1/appointments/{id}`       | Get appointment             |
| `PATCH`  | `/api/v1/appointments/{id}`       | Update appointment          |
| `GET`    | `/api/v1/observations/`           | List observations           |
| `POST`   | `/api/v1/observations/`           | Create observation          |
| `GET`    | `/api/v1/observations/{id}`       | Get observation             |

### Query Parameters

- **Patients**: `search`, `active`, `skip`, `limit`
- **Practitioners**: `specialty`, `skip`, `limit`
- **Appointments**: `patient_id`, `practitioner_id`, `status`, `skip`, `limit`
- **Observations**: `patient_id`, `code`, `skip`, `limit`

## Data Models

The data layer uses FHIR-inspired resource types:

- **Patient** — demographics, contact info, insurance, allergies
- **Practitioner** — NPI-identified providers with specialty/department
- **Appointment** — links patient + practitioner with status workflow
- **Observation** — clinical measurements using LOINC-style coding (heart rate, blood pressure, glucose, HbA1c, etc.)

## Project Structure

```
healthcare-modernization/
├── docker-compose.yml          # Full-stack orchestration
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── main.py             # FastAPI app + CORS + lifespan
│       ├── config.py           # Pydantic settings
│       ├── database.py         # SQLAlchemy engine + session
│       ├── seed.py             # Sample data seeder
│       ├── models/             # SQLAlchemy ORM models
│       ├── schemas/            # Pydantic request/response schemas
│       └── routers/            # API route handlers
├── frontend/
│   ├── Dockerfile + nginx.conf
│   ├── package.json
│   └── src/
│       ├── App.tsx             # Routes
│       ├── api/client.ts       # Typed API client
│       ├── types/index.ts      # TypeScript interfaces
│       ├── components/         # Shared UI components
│       └── pages/              # Page components
└── docs/
    └── architecture.md
```

## License

MIT
