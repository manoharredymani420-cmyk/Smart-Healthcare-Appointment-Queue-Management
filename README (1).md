# MediCare — Smart Healthcare Appointment & Queue Management Platform

> A portfolio-grade Python full-stack healthcare application for appointment management, doctor scheduling, digital queue tracking, patient records, analytics, and machine-learning-based waiting-time estimation.

**Project status:** Planned / Development  
**Primary developer:** Manohar  
**Target:** Python Full Stack + Data Science portfolio project

---

## 1. Project Overview

MediCare is a web-based healthcare management platform designed to reduce manual appointment work and improve visibility into patient queues.

The system will provide separate experiences for:

- Patients
- Doctors
- Clinic administrators

The application will manage appointments, doctor availability, queue status, basic patient records, and analytics.

A later phase will add a machine-learning model that estimates patient waiting time using historical appointment and queue data.

### Important scope

This is an educational/portfolio project. It will use synthetic or dummy data and must not be used for real medical diagnosis, treatment decisions, or storage of real patient health information.

---

## 2. Problem Statement

Small clinics and healthcare centers may rely on manual appointment registers, phone calls, spreadsheets, or disconnected systems.

This can create problems such as:

- Appointment conflicts
- Unclear doctor availability
- Long and unpredictable waiting times
- Difficult queue tracking
- Poor visibility into daily clinic operations
- Limited appointment analytics

MediCare will provide one centralized application for these workflows.

---

## 3. Goals

### Primary goals

1. Build a clean Python full-stack application.
2. Implement a proper REST API.
3. Design a normalized relational database.
4. Provide role-based dashboards.
5. Implement appointment booking and cancellation.
6. Implement digital queue management.
7. Add waiting-time estimation.
8. Add analytics and charts.
9. Add automated tests.
10. Document the complete system.
11. Containerize the application.
12. Deploy a working demo.
13. Maintain the project using Git/GitHub and feature branches.

### Portfolio goals

The project should demonstrate:

- Python
- Flask
- REST API development
- PostgreSQL
- SQL
- JavaScript
- HTML/CSS
- Authentication
- Database design
- Machine learning
- Testing
- Docker
- Git/GitHub
- API documentation
- Deployment
- Professional documentation

---

## 4. Technology Stack

### Backend

- Python 3.12+
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-CORS
- Flask-JWT-Extended
- Marshmallow or Pydantic for validation
- Gunicorn for production serving

### Frontend

- HTML5
- CSS3
- JavaScript ES6+
- Bootstrap
- Fetch API
- Chart.js

### Database

- PostgreSQL
- SQLite for lightweight local development/testing if required

### Data Science

- Pandas
- NumPy
- scikit-learn
- Joblib
- Matplotlib / Plotly for analysis

### Testing

- pytest
- Postman

### DevOps

- Docker
- Docker Compose
- GitHub Actions

### Development

- Antigravity
- VS Code or another editor
- Git
- GitHub

---

## 5. High-Level Architecture

```text
                         ┌──────────────────────────┐
                         │          USERS           │
                         │ Patient / Doctor / Admin │
                         └────────────┬─────────────┘
                                      │
                                      ▼
                         ┌──────────────────────────┐
                         │       FRONTEND           │
                         │ HTML / CSS / JavaScript  │
                         │ Bootstrap / Chart.js     │
                         └────────────┬─────────────┘
                                      │
                               HTTP / JSON
                                      │
                                      ▼
                         ┌──────────────────────────┐
                         │      FLASK REST API      │
                         │                          │
                         │ Auth                      │
                         │ Users                     │
                         │ Doctors                   │
                         │ Appointments              │
                         │ Queue                     │
                         │ Medical Records           │
                         │ Analytics                 │
                         │ ML Prediction             │
                         └───────┬───────────┬──────┘
                                 │           │
                         SQLAlchemy           │
                                 │           │
                    ┌────────────▼───┐   ┌───▼────────────────┐
                    │   PostgreSQL   │   │  ML Prediction     │
                    │                │   │  Service           │
                    │ Users          │   │                    │
                    │ Patients       │   │ Waiting-time model │
                    │ Doctors        │   │ Model artifacts    │
                    │ Departments    │   └────────────────────┘
                    │ Appointments   │
                    │ Queue Records  │
                    │ Medical Records│
                    └────────────────┘
```

---

## 6. User Roles

### Patient

Can:

- Register
- Login
- Update profile
- Search doctors
- View doctor availability
- Book appointment
- Cancel appointment
- View appointment history
- View queue status
- View estimated waiting time
- View permitted visit history

### Doctor

Can:

- Login
- View profile
- View daily appointments
- View current queue
- Call the next patient
- Mark appointment as completed
- Add consultation notes for the demo dataset
- View previous appointment information permitted by the application

### Admin

Can:

- Login
- Manage users
- Manage doctors
- Manage departments
- View appointments
- Manage clinic schedules
- Monitor queues
- View analytics
- Manage system configuration

---

## 7. Core Modules

### Module 1 — Authentication

Features:

- Registration
- Login
- Password hashing
- JWT authentication
- Role-based authorization
- Logout/token invalidation strategy
- Input validation

API examples:

```text
POST /api/auth/register
POST /api/auth/login
GET  /api/auth/me
```

---

### Module 2 — Patient Management

Features:

- Patient profile
- Contact information
- Appointment history
- Basic demographic information
- Account status

---

### Module 3 — Doctor Management

Features:

- Doctor profile
- Specialization
- Department
- Availability
- Appointment capacity
- Daily schedule

---

### Module 4 — Department Management

Example departments:

- General Medicine
- Pediatrics
- Dermatology
- Orthopedics
- Cardiology

These are demonstration categories only.

---

### Module 5 — Appointment Management

Features:

- Search doctors
- Select date
- View available slots
- Book appointment
- Generate token number
- Cancel appointment
- Reschedule appointment
- Appointment status

Possible statuses:

```text
BOOKED
CONFIRMED
WAITING
IN_PROGRESS
COMPLETED
CANCELLED
NO_SHOW
```

---

### Module 6 — Digital Queue

The queue module will track:

```text
Token number
Appointment
Doctor
Date
Queue position
Patients ahead
Status
Estimated waiting time
```

Example:

```text
Token: 18
Patients ahead: 4
Average consultation: 8 minutes
Estimated wait: approximately 32 minutes
```

The first version can use a deterministic calculation. The ML model will be added later.

---

### Module 7 — Medical/Visit Records

For portfolio demonstration only.

Fields may include:

```text
Appointment
Doctor
Patient
Visit date
Diagnosis/demo label
Consultation notes
Follow-up date
```

Do not use real patient information.

The application must display a clear educational-use notice.

---

### Module 8 — Analytics

Admin dashboard metrics:

- Total appointments
- Completed appointments
- Cancelled appointments
- No-show count
- Appointments by department
- Appointments by day
- Average waiting time
- Queue length
- Doctor appointment load

Charts will use Chart.js.

---

### Module 9 — ML Waiting-Time Prediction

The ML system will estimate waiting time.

Possible features:

```text
doctor_id
department_id
day_of_week
appointment_hour
patients_ahead
current_queue_length
average_consultation_time
appointments_scheduled
historical_average_wait
```

Target:

```text
waiting_time_minutes
```

Candidate models:

- Linear Regression
- Random Forest Regressor
- Gradient Boosting Regressor

We will compare models using:

- MAE
- RMSE
- R²

The best model will be selected based on measured validation/test performance, not an assumed winner.

Model files will be saved with Joblib.

---

## 8. Database Design

### users

```text
id
name
email
password_hash
role
is_active
created_at
updated_at
```

### patients

```text
id
user_id
date_of_birth
gender
phone
address
created_at
updated_at
```

### doctors

```text
id
user_id
department_id
specialization
experience_years
consultation_duration_minutes
is_available
created_at
updated_at
```

### departments

```text
id
name
description
created_at
```

### doctor_schedules

```text
id
doctor_id
day_of_week
start_time
end_time
slot_duration_minutes
max_appointments
```

### appointments

```text
id
patient_id
doctor_id
appointment_date
appointment_time
token_number
status
reason
created_at
updated_at
```

### queue_records

```text
id
appointment_id
doctor_id
queue_position
patients_ahead
estimated_wait_minutes
queue_status
created_at
updated_at
```

### medical_records

```text
id
patient_id
doctor_id
appointment_id
visit_date
diagnosis_demo
notes
follow_up_date
created_at
updated_at
```

### prediction_logs

```text
id
appointment_id
model_version
predicted_wait_minutes
actual_wait_minutes
prediction_created_at
```

---

## 9. API Design

Base URL:

```text
/api
```

### Authentication

```text
POST /api/auth/register
POST /api/auth/login
GET  /api/auth/me
```

### Patients

```text
GET  /api/patients/me
PUT  /api/patients/me
GET  /api/patients/me/appointments
GET  /api/patients/me/records
```

### Doctors

```text
GET /api/doctors
GET /api/doctors/<id>
GET /api/doctors/<id>/availability
GET /api/doctors/<id>/appointments
GET /api/doctors/<id>/queue
```

### Appointments

```text
POST   /api/appointments
GET    /api/appointments/<id>
PUT    /api/appointments/<id>
DELETE /api/appointments/<id>
```

### Queue

```text
GET /api/queue/<appointment_id>
POST /api/queue/<appointment_id>/next
PUT /api/queue/<appointment_id>/status
```

### Analytics

```text
GET /api/analytics/overview
GET /api/analytics/appointments
GET /api/analytics/waiting-times
GET /api/analytics/departments
```

### ML

```text
POST /api/predictions/waiting-time
GET  /api/predictions/<appointment_id>
```

---

## 10. Frontend Pages

```text
/
├── index.html
├── login.html
├── register.html
├── patient/
│   ├── dashboard.html
│   ├── doctors.html
│   ├── book-appointment.html
│   ├── appointments.html
│   ├── queue.html
│   └── records.html
├── doctor/
│   ├── dashboard.html
│   ├── appointments.html
│   ├── queue.html
│   └── patients.html
└── admin/
    ├── dashboard.html
    ├── users.html
    ├── doctors.html
    ├── departments.html
    ├── appointments.html
    └── analytics.html
```

---

## 11. Backend Structure

Recommended structure:

```text
backend/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── extensions.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── patient.py
│   │   ├── doctor.py
│   │   ├── department.py
│   │   ├── schedule.py
│   │   ├── appointment.py
│   │   ├── queue.py
│   │   ├── medical_record.py
│   │   └── prediction.py
│   │
│   ├── routes/
│   │   ├── auth.py
│   │   ├── patients.py
│   │   ├── doctors.py
│   │   ├── appointments.py
│   │   ├── queue.py
│   │   ├── analytics.py
│   │   └── predictions.py
│   │
│   ├── services/
│   │   ├── appointment_service.py
│   │   ├── queue_service.py
│   │   ├── prediction_service.py
│   │   └── notification_service.py
│   │
│   ├── schemas/
│   │   └── ...
│   │
│   └── utils/
│       ├── errors.py
│       ├── decorators.py
│       └── security.py
│
├── migrations/
├── tests/
├── seed.py
├── run.py
└── requirements.txt
```

---

## 12. Frontend Structure

```text
frontend/
├── index.html
├── pages/
├── css/
│   ├── style.css
│   ├── dashboard.css
│   └── responsive.css
├── js/
│   ├── api.js
│   ├── auth.js
│   ├── appointments.js
│   ├── queue.js
│   ├── dashboard.js
│   └── charts.js
└── assets/
```

---

## 13. Security Requirements

This is a portfolio project, but basic security practices should still be followed.

Implement:

- Password hashing
- JWT authentication
- Role-based access control
- Server-side validation
- Parameterized database queries through SQLAlchemy
- CORS configuration
- Environment variables
- No secrets in Git
- `.env.example`
- Safe error responses
- Request validation
- Basic rate limiting if practical

Never commit:

```text
.env
passwords
API keys
JWT secrets
real patient data
```

---

## 14. Testing

Create tests for:

### Authentication

- Registration
- Login
- Invalid credentials
- Protected endpoint

### Appointments

- Valid booking
- Duplicate/conflicting booking
- Cancellation
- Invalid doctor
- Invalid date/time

### Queue

- Token creation
- Queue ordering
- Patients ahead calculation
- Status transitions

### ML

- Model loads correctly
- Prediction returns numeric output
- Invalid input is rejected

Target an increasing test coverage over the project lifecycle.

---

## 15. Docker

Services:

```text
frontend
backend
postgres
```

Optional later:

```text
nginx
```

Example architecture:

```text
Browser
   │
   ▼
Frontend / Web Server
   │
   ▼
Flask API
   │
   ├──── PostgreSQL
   │
   └──── ML Model
```

---

## 16. Git Workflow

Use feature branches.

Example:

```text
main
│
├── develop
│
├── feature/authentication
├── feature/appointments
├── feature/queue
├── feature/dashboard
├── feature/ml-prediction
└── feature/testing
```

Commit examples:

```text
feat: add user authentication
feat: add doctor availability API
feat: implement appointment booking
feat: implement digital queue
feat: add waiting time prediction
test: add appointment API tests
docs: update API documentation
fix: prevent duplicate appointment slots
```

---

## 17. Development Roadmap

### Phase 1 — Project setup

- Create GitHub repository
- Create folders
- Create virtual environment
- Install dependencies
- Configure Flask
- Configure environment variables
- Create README

### Phase 2 — Database

- Configure PostgreSQL
- Create SQLAlchemy models
- Add migrations
- Create seed data
- Test relationships

### Phase 3 — Authentication

- Registration
- Password hashing
- Login
- JWT
- Role authorization

### Phase 4 — Doctor & Department

- CRUD APIs
- Doctor availability
- Schedule management

### Phase 5 — Appointments

- Slot generation
- Booking
- Cancellation
- Rescheduling
- Token generation

### Phase 6 — Queue

- Queue creation
- Queue ordering
- Current patient
- Patients ahead
- Estimated waiting time

### Phase 7 — Frontend

- Login
- Patient dashboard
- Doctor dashboard
- Admin dashboard
- Appointment UI
- Queue UI

### Phase 8 — Analytics

- Charts
- KPIs
- Appointment reports
- Waiting-time reports

### Phase 9 — ML

- Generate/prepare synthetic dataset
- Data cleaning
- Feature engineering
- Train multiple regressors
- Evaluate
- Save model
- Create prediction API
- Integrate with queue

### Phase 10 — Quality

- Unit tests
- API tests
- Error handling
- Logging
- Validation
- Security review

### Phase 11 — Deployment

- Docker
- Docker Compose
- CI/CD
- Cloud deployment
- Production configuration

### Phase 12 — Portfolio

- Screenshots
- Architecture diagram
- API documentation
- Demo video
- Final README
- Resume project description

---

## 18. Antigravity Development Instructions

Use Antigravity as the development environment/AI coding assistant, but keep the architecture and source of truth in this repository.

Before generating code, Antigravity should:

1. Read `README.md`.
2. Read `ARCHITECTURE.md`.
3. Read the current project structure.
4. Never rewrite working modules without checking dependencies.
5. Work one feature at a time.
6. Run tests after significant changes.
7. Keep secrets out of source code.
8. Update documentation when APIs or architecture change.
9. Use Git feature branches.
10. Explain important implementation decisions.

### Recommended Antigravity prompt

```text
You are working on the MediCare Smart Healthcare Appointment & Queue
Management Platform.

First read:
- README.md
- ARCHITECTURE.md
- PROJECT_PLAN.md

Do not generate the entire application at once.

Work only on the current phase/task.

Requirements:
1. Follow the existing architecture.
2. Use Python + Flask + SQLAlchemy + PostgreSQL.
3. Use REST APIs with JSON responses.
4. Validate input on the server.
5. Implement proper error handling.
6. Write tests for new backend functionality.
7. Do not hard-code passwords, API keys, or secrets.
8. Do not use real patient data.
9. Keep functions modular and maintainable.
10. Update documentation when a public API or database design changes.

Before coding:
- inspect the current repository
- identify affected files
- explain the implementation plan

After coding:
- run the relevant tests
- report files changed
- report tests executed
- report any remaining issues
```

---

## 19. Definition of Done

A feature is not complete merely because the code runs.

A feature is complete when:

```text
[ ] Backend implemented
[ ] Database integration completed
[ ] Validation added
[ ] Error handling added
[ ] API tested
[ ] Frontend integrated
[ ] Tests written
[ ] Documentation updated
[ ] Git commit created
```

---

## 20. Future Enhancements

Possible later additions:

- Email appointment reminders
- SMS notifications
- Calendar integration
- Doctor-to-doctor referral workflow
- Advanced analytics
- Explainable ML
- Multi-clinic support
- Audit logs
- Redis caching
- Background jobs
- WebSocket-based live queue updates
- Mobile application
- OpenAPI/Swagger documentation

These should be added only after the core application is stable.

---

## 21. Portfolio Outcome

At completion, the project should demonstrate:

```text
Python
   +
Flask
   +
REST APIs
   +
PostgreSQL
   +
JavaScript
   +
Machine Learning
   +
Testing
   +
Docker
   +
Git/GitHub
   +
Deployment
```

The goal is to demonstrate the ability to build, test, document, and deploy a real full-stack application—not simply produce a collection of screens.

---

## 22. Disclaimer

MediCare is an educational software project.

It is not a medical device and does not provide medical diagnosis, treatment recommendations, or emergency medical services.

Use synthetic/demo data only.
