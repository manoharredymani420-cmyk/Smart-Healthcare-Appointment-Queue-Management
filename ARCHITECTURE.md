# MediCare — Architecture Specification

## 1. Architecture Principle

MediCare uses a modular three-layer application architecture:

```text
Presentation Layer
        │
        ▼
Application/API Layer
        │
        ▼
Data + ML Layer
```

The system should remain modular so that the frontend, backend, database and ML components can evolve independently.

---

## 2. Complete System Architecture

```text
                         ┌─────────────────────┐
                         │       PATIENT       │
                         └──────────┬──────────┘
                                    │
                         ┌──────────▼──────────┐
                         │       DOCTOR        │
                         └──────────┬──────────┘
                                    │
                         ┌──────────▼──────────┐
                         │       ADMIN         │
                         └──────────┬──────────┘
                                    │
                                    ▼
                 ┌──────────────────────────────────┐
                 │          WEB FRONTEND             │
                 │                                  │
                 │ HTML5 + CSS3 + JS + Bootstrap    │
                 │ Fetch API + Chart.js             │
                 └────────────────┬─────────────────┘
                                  │ HTTPS / JSON
                                  ▼
                 ┌──────────────────────────────────┐
                 │            FLASK API             │
                 │                                  │
                 │ Authentication                   │
                 │ Users / Patients / Doctors       │
                 │ Appointments                      │
                 │ Queue                             │
                 │ Records                           │
                 │ Analytics                         │
                 │ Predictions                       │
                 └───────────────┬──────────────────┘
                                 │
                    ┌────────────┴────────────┐
                    │                         │
                    ▼                         ▼
          ┌──────────────────┐      ┌──────────────────┐
          │   PostgreSQL     │      │   ML Service     │
          │                  │      │                  │
          │ Relational Data  │      │ scikit-learn     │
          │                  │      │ Joblib Model     │
          └──────────────────┘      └──────────────────┘
```

---

## 3. Request Flow

Example: patient books an appointment.

```text
Patient
  │
  │ clicks "Book"
  ▼
JavaScript
  │
  │ POST /api/appointments
  │ JSON payload
  ▼
Flask Route
  │
  ▼
Authentication
  │
  ▼
Request Validation
  │
  ▼
Appointment Service
  │
  ├── Check doctor
  ├── Check schedule
  ├── Check slot conflict
  └── Generate token
  │
  ▼
SQLAlchemy
  │
  ▼
PostgreSQL
  │
  ▼
Queue Service
  │
  ▼
Waiting-Time Service
  │
  ▼
JSON Response
  │
  ▼
JavaScript
  │
  ▼
Patient Dashboard
```

---

## 4. Backend Layers

### Route Layer

Responsible for:

- HTTP request/response
- Authentication decorators
- Calling services
- Returning JSON

Routes should not contain large business-logic blocks.

### Service Layer

Responsible for:

- Appointment rules
- Queue calculation
- Availability rules
- Prediction integration
- Business logic

### Model Layer

Responsible for:

- Database entities
- Relationships
- Constraints

### Utility Layer

Responsible for:

- Security
- Errors
- Common helpers
- Validation helpers

---

## 5. Database Relationships

```text
users
 │
 ├──────────────► patients
 │
 └──────────────► doctors
                       │
                       ├────────────► departments
                       │
                       └────────────► doctor_schedules

patients ─────────────► appointments ◄──────────── doctors
                              │
                              ├────────► queue_records
                              │
                              └────────► medical_records

appointments ─────────► prediction_logs
```

---

## 6. Authentication Flow

```text
Login
 │
 ▼
POST /api/auth/login
 │
 ▼
Find user
 │
 ▼
Verify password hash
 │
 ▼
Generate JWT
 │
 ▼
Return token
 │
 ▼
Frontend stores token securely according to deployment strategy
 │
 ▼
Subsequent API requests include Authorization header
```

Authorization rules:

```text
PATIENT → patient endpoints
DOCTOR  → doctor endpoints
ADMIN   → administrative endpoints
```

The server must enforce authorization. Hiding a frontend button is not sufficient security.

---

## 7. Appointment State Machine

```text
BOOKED
  │
  ▼
CONFIRMED
  │
  ▼
WAITING
  │
  ▼
IN_PROGRESS
  │
  ▼
COMPLETED
```

Alternative paths:

```text
BOOKED ─────► CANCELLED
CONFIRMED ──► CANCELLED
CONFIRMED ──► NO_SHOW
```

The API should reject invalid state transitions.

---

## 8. Queue Algorithm — Version 1

For the initial version:

```text
patients_ahead =
    number of active appointments before current patient
```

Then:

```text
estimated_wait =
    patients_ahead × average_consultation_duration
```

Example:

```text
Patients ahead = 4
Average duration = 10 minutes

Estimated wait = 40 minutes
```

This is a baseline, not a medical prediction.

---

## 9. ML Architecture

### Training

```text
Historical/Synthetic Dataset
          │
          ▼
Data Validation
          │
          ▼
Cleaning
          │
          ▼
Feature Engineering
          │
          ▼
Train/Test Split
          │
          ▼
Model Training
     ┌────┼────┐
     ▼    ▼    ▼
Linear RF  Gradient
Regression Forest Boosting
     └────┼────┘
          ▼
Model Evaluation
          │
          ▼
Select based on validation/test metrics
          │
          ▼
Save model.joblib
```

### Inference

```text
Appointment
    │
    ▼
Feature Builder
    │
    ▼
Saved Model
    │
    ▼
Predicted waiting time
    │
    ▼
API response
```

---

## 10. API Error Format

Use a consistent structure:

```json
{
  "success": false,
  "error": {
    "code": "APPOINTMENT_CONFLICT",
    "message": "The selected slot is not available."
  }
}
```

Successful response:

```json
{
  "success": true,
  "data": {
    "appointment_id": 101,
    "token_number": 18,
    "status": "BOOKED"
  }
}
```

---

## 11. Configuration

Use environment variables.

Example:

```text
FLASK_ENV=
SECRET_KEY=
JWT_SECRET_KEY=
DATABASE_URL=
CORS_ORIGINS=
```

Never commit real values.

Provide:

```text
.env.example
```

---

## 12. Observability

The backend should eventually include:

- Structured application logs
- Request logging
- Error logging
- Prediction logging
- Database error handling

Do not log passwords, JWT secrets, or sensitive patient information.

---

## 13. Deployment Architecture

Initial deployment:

```text
Internet
   │
   ▼
Frontend/Web Server
   │
   ▼
Flask/Gunicorn
   │
   ├──── PostgreSQL
   │
   └──── Model Files
```

Later:

```text
Internet
   │
   ▼
Reverse Proxy
   │
   ├──────── Frontend
   │
   └──────── API
                │
                ├── PostgreSQL
                ├── Redis
                └── Background Worker
```

---

## 14. Non-Functional Requirements

### Performance

- Avoid unnecessary database queries.
- Add indexes to frequently queried fields.
- Paginate large lists.
- Keep API responses small.

### Reliability

- Validate all important inputs.
- Handle database errors.
- Return consistent API errors.
- Add automated tests.

### Security

- Hash passwords.
- Use authorization.
- Protect secrets.
- Avoid real patient data.
- Configure CORS deliberately.

### Maintainability

- Modular backend.
- Small service functions.
- Clear naming.
- Type hints where useful.
- Documentation.
- Tests.

---

## 15. Architecture Decision

The first release will remain a modular monolith.

Why:

```text
Simpler development
       +
Easy local setup
       +
Easy deployment
       +
Good for a fresher portfolio
```

Microservices are intentionally postponed until there is a demonstrated need.
