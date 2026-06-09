# Architecture Overview

## Design Principles

1. **FHIR-Inspired Models** — Data models are loosely based on HL7 FHIR resource types (Patient, Practitioner, Observation) to demonstrate healthcare interoperability patterns without requiring full FHIR compliance.

2. **API-First** — The backend exposes a clean REST API with versioning (`/api/v1/`), automatic OpenAPI docs, and Pydantic validation. The frontend consumes this API through a typed client.

3. **Separation of Concerns** — Clear boundaries between data layer (SQLAlchemy models), validation (Pydantic schemas), and routing (FastAPI routers).

4. **Modern Frontend** — React with TypeScript, component-based architecture, TailwindCSS utility classes, and client-side routing via React Router.

## Technology Choices

### Why FastAPI?
- Native async support for high-throughput healthcare workloads
- Automatic OpenAPI/Swagger documentation — critical for healthcare API integrations
- Pydantic-based validation ensures data integrity at the API boundary
- Strong typing that pairs well with TypeScript on the frontend

### Why PostgreSQL?
- ACID compliance — essential for healthcare data integrity
- UUID primary keys — standard for distributed healthcare systems
- JSON support for flexible clinical data (future enhancement)
- Battle-tested in regulated environments

### Why React + TypeScript?
- Type safety across the full stack
- Component reusability for complex healthcare UIs
- Large ecosystem of accessible UI components

## Data Flow

```
User → React Router → Page Component → API Client (fetch)
                                              ↓
                                    FastAPI Router → SQLAlchemy → PostgreSQL
                                              ↓
                                    Pydantic Schema (response)
                                              ↓
                                    React State → UI Update
```

## Future Enhancements

- [ ] Full FHIR R4 compliance with resource bundles
- [ ] HL7v2 message ingestion pipeline
- [ ] Role-based access control (RBAC) with OAuth2/OIDC
- [ ] Audit logging for HIPAA compliance
- [ ] Real-time notifications via WebSocket
- [ ] Telehealth video integration
- [ ] Patient portal with self-service scheduling
- [ ] Analytics dashboard with population health metrics
