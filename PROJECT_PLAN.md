# MediCare — Development Plan for Antigravity

## Objective

Build MediCare incrementally as a professional Python full-stack project.

Do not ask the AI coding assistant to generate the complete application in one step.

---

# Phase 0 — Rules

Before coding:

1. Read `README.md`.
2. Read `ARCHITECTURE.md`.
3. Read this file.
4. Inspect existing files.
5. Never overwrite working code blindly.
6. Work on one feature at a time.
7. Run tests after changes.
8. Update documentation when behavior changes.
9. Use synthetic data only.
10. Never expose secrets.

---

# Phase 1 — Repository

Tasks:

- Create Git repository
- Add README
- Add ARCHITECTURE
- Add PROJECT_PLAN
- Add `.gitignore`
- Add `.env.example`
- Add LICENSE
- Add CONTRIBUTING.md

Commit:

```text
docs: initialize project documentation
```

---

# Phase 2 — Backend Foundation

Tasks:

- Create Python virtual environment
- Create Flask application factory
- Add configuration
- Add extensions
- Add health endpoint
- Add error handler
- Add CORS configuration
- Add requirements.txt

First endpoint:

```text
GET /api/health
```

Expected:

```json
{
  "success": true,
  "message": "MediCare API is running"
}
```

---

# Phase 3 — PostgreSQL

Tasks:

- Configure PostgreSQL
- Configure SQLAlchemy
- Configure Flask-Migrate
- Create User model
- Create Patient model
- Create Doctor model
- Create Department model
- Create Schedule model
- Create Appointment model
- Create Queue model
- Create MedicalRecord model
- Create PredictionLog model
- Create migrations
- Create seed data

---

# Phase 4 — Authentication

Tasks:

- Register
- Login
- Password hashing
- JWT
- Current user endpoint
- Role authorization

Tests:

```text
register valid
register duplicate email
login valid
login invalid
protected endpoint
wrong role
```

---

# Phase 5 — Doctors and Departments

Tasks:

- Department CRUD
- Doctor listing
- Doctor details
- Doctor schedules
- Availability calculation

---

# Phase 6 — Appointments

Tasks:

- Generate available slots
- Book appointment
- Prevent conflicting appointments
- Generate token
- Cancel
- Reschedule
- Appointment history

Tests must cover conflict cases.

---

# Phase 7 — Queue

Tasks:

- Create queue record
- Calculate position
- Calculate patients ahead
- Current patient
- Next patient
- Status changes
- Waiting-time baseline

---

# Phase 8 — Frontend

Tasks:

- Landing page
- Login
- Register
- Patient dashboard
- Doctor dashboard
- Admin dashboard
- Doctor search
- Booking page
- Appointment history
- Queue page
- Analytics

Use Fetch API to communicate with Flask.

---

# Phase 9 — Analytics

Create:

```text
GET /api/analytics/overview
GET /api/analytics/appointments
GET /api/analytics/waiting-times
GET /api/analytics/departments
```

Frontend charts:

- Daily appointments
- Department distribution
- Waiting-time trend
- Completion/cancellation breakdown

---

# Phase 10 — ML Dataset

Create a synthetic dataset.

Possible columns:

```text
doctor_id
department_id
day_of_week
appointment_hour
patients_ahead
queue_length
average_consultation_time
appointments_scheduled
historical_average_wait
waiting_time_minutes
```

Do not claim that synthetic data represents real hospital performance.

---

# Phase 11 — ML Training

Train:

```text
LinearRegression
RandomForestRegressor
GradientBoostingRegressor
```

Evaluate:

```text
MAE
RMSE
R2
```

Save the selected model.

Also save the preprocessing pipeline if preprocessing is used.

---

# Phase 12 — ML API

Implement:

```text
POST /api/predictions/waiting-time
```

Input:

```json
{
  "doctor_id": 5,
  "department_id": 2,
  "patients_ahead": 4,
  "queue_length": 6,
  "appointment_hour": 10
}
```

Return:

```json
{
  "success": true,
  "prediction": {
    "estimated_wait_minutes": 34,
    "model_version": "v1"
  }
}
```

---

# Phase 13 — Testing

Use pytest.

Target:

- Unit tests
- API tests
- Authentication tests
- Database tests
- Queue tests
- ML prediction tests

Add tests before calling the project complete.

---

# Phase 14 — Docker

Create:

```text
Dockerfile
docker-compose.yml
```

Services:

```text
backend
postgres
```

Frontend may initially be served by the backend or a simple web server.

---

# Phase 15 — CI

GitHub Actions should:

```text
checkout
↓
install Python
↓
install dependencies
↓
run lint/checks
↓
run tests
```

---

# Phase 16 — Deployment

Deploy:

- Backend
- PostgreSQL
- Frontend

Configure production environment variables.

Verify:

```text
register
login
book appointment
queue
dashboard
prediction
```

---

# Phase 17 — Portfolio

Add to GitHub:

- Screenshots
- Architecture diagram
- API examples
- Database diagram
- Test results
- Live demo
- Demo video
- Setup instructions
- Known limitations
- Future roadmap

---

# Antigravity Prompt — Phase-by-Phase

Use this prompt before each development task:

```text
We are building the MediCare Smart Healthcare Appointment & Queue
Management Platform.

Read README.md, ARCHITECTURE.md and PROJECT_PLAN.md first.

Current phase:
[PUT PHASE HERE]

Current task:
[PUT TASK HERE]

Instructions:
1. Inspect the repository before changing anything.
2. Follow the documented architecture.
3. Do not generate unrelated features.
4. Do not rewrite working code unnecessarily.
5. Keep backend routes, services and models separated.
6. Use SQLAlchemy for database access.
7. Validate API input.
8. Return consistent JSON responses.
9. Add tests for new behavior.
10. Do not use real patient data.
11. Never hard-code secrets.
12. Update documentation if the public API/database changes.

Before coding:
- Tell me which files will be created/modified.
- Explain the implementation briefly.

After coding:
- Run the relevant tests.
- Show the test result.
- List changed files.
- Mention any known limitations.
```

---

# Completion Checklist

## Foundation

- [ ] Repository created
- [ ] Flask app runs
- [ ] Health endpoint works
- [ ] PostgreSQL connected

## Authentication

- [ ] Register
- [ ] Login
- [ ] JWT
- [ ] Roles
- [ ] Tests

## Core

- [ ] Doctors
- [ ] Departments
- [ ] Schedules
- [ ] Appointments
- [ ] Queue
- [ ] Records

## Frontend

- [ ] Patient dashboard
- [ ] Doctor dashboard
- [ ] Admin dashboard
- [ ] Booking
- [ ] Queue

## ML

- [ ] Dataset
- [ ] Preprocessing
- [ ] Multiple models
- [ ] Evaluation
- [ ] Model artifact
- [ ] Prediction API

## Engineering

- [ ] Tests
- [ ] Logging
- [ ] Docker
- [ ] CI
- [ ] API docs
- [ ] Deployment

## Portfolio

- [ ] README
- [ ] Architecture diagram
- [ ] Screenshots
- [ ] Demo
- [ ] Git history
- [ ] Resume description
