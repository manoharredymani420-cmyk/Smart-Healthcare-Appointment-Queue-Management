# MediCare — Smart Healthcare Appointment & Digital Queue Platform

> **A Complete Python Full-Stack & Machine Learning Healthcare System** featuring intelligent appointment scheduling, slot conflict prevention, real-time digital queue management, ML-based waiting-time estimation (Gradient Boosting Regressor), role-based dashboards (Patient, Doctor, Administrator), operational analytics charts, and comprehensive REST APIs.

---

## Table of Contents
1. [Project Overview & Architecture](#1-project-overview--architecture)
2. [Steps to Run the Service Locally](#2-steps-to-run-the-service-locally)
3. [Pre-Configured Demo User Credentials](#3-pre-configured-demo-user-credentials)
4. [In-Depth Feature Documentation](#4-in-depth-feature-documentation)
5. [Complete REST API Specification](#5-complete-rest-api-specification)
6. [Database Schema & Data Models](#6-database-schema--data-models)
7. [Machine Learning Pipeline & Evaluation](#7-machine-learning-pipeline--evaluation)
8. [Automated Testing Guide](#8-automated-testing-guide)
9. [Docker Deployment](#9-docker-deployment)
10. [Security & Educational Disclaimer](#10-security--educational-disclaimer)

---

## 1. Project Overview & Architecture

MediCare is engineered to solve the persistent operational challenges faced by outpatient clinics: crowded waiting rooms, unpredictable consultation delays, double-booking conflicts, and lack of real-time queue visibility.

### Three-Layer Modular Architecture

```text
┌────────────────────────────────────────────────────────┐
│                   PRESENTATION LAYER                   │
│  HTML5 + CSS3 + Bootstrap 5 + Vanilla JS + Chart.js    │
│  Patient Portal  │  Doctor Portal  │  Admin Analytics  │
└───────────────────────────┬────────────────────────────┘
                            │ HTTPS / JSON (JWT Bearer)
                            ▼
┌────────────────────────────────────────────────────────┐
│                  APPLICATION / API LAYER               │
│                     Flask Application                  │
│  ┌─────────────────┐ ┌──────────────────────────────┐  │
│  │   Auth & RBAC   │ │ Appointment & Queue Services │  │
│  └─────────────────┘ └──────────────────────────────┘  │
│  ┌─────────────────┐ ┌──────────────────────────────┐  │
│  │ Analytics Engine│ │   ML Inference Service       │  │
│  └─────────────────┘ └──────────────────────────────┘  │
└─────────────┬───────────────────────────┬──────────────┘
              │ SQLAlchemy ORM            │ Joblib
              ▼                           ▼
┌──────────────────────────┐ ┌───────────────────────────┐
│     RELATIONAL DATA      │ │         ML MODEL          │
│   SQLite / PostgreSQL    │ │ GradientBoostingRegressor │
│  Users, Patients,        │ │ (R² = 0.9938,             │
│  Doctors, Appointments,  │ │  MAE = 3.45 minutes)      │
│  Queue, Medical Records  │ │                           │
└──────────────────────────┘ └───────────────────────────┘
```

---

## 2. Steps to Run the Service Locally

Follow these step-by-step instructions to run the application on your local machine with zero compilation errors.

### Prerequisites
- **Python 3.12+** installed (`python --version` or `py --version`)
- **Git** (optional, for version control)

### Step 1: Open Terminal in Project Directory
Navigate to the root directory of the project:
```powershell
cd "d:\Smart Healthcare Appointment & Queue Management"
```

### Step 2: Create and Activate a Python Virtual Environment
**On Windows PowerShell:**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```
*(If PowerShell restricts scripts, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` first).*

**On macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Required Dependencies
```powershell
pip install -r requirements.txt
```
*Dependencies installed include: Flask, Flask-SQLAlchemy, Flask-CORS, Flask-JWT-Extended, scikit-learn, joblib, pandas, numpy, pytest, python-dotenv.*

### Step 4: Train the ML Model Artifact
MediCare includes an automated synthetic clinic training pipeline that compares Multiple Regressors and saves the best model:
```powershell
python -m ml.train
```
*Output: Compares Linear Regression, Random Forest, and Gradient Boosting models, logging MAE, RMSE, and R² scores, and generates `ml/model.joblib`.*

### Step 5: Initialize and Seed the Database
Populate the database with pre-configured departments, physicians with working schedules, patients, queue tickets, and medical visit records:
```powershell
python seed.py
```
*Output: `Database successfully seeded with realistic healthcare clinic data!`*

### Step 6: Start the Local Web Server
Launch the application:
```powershell
python run.py
```

### Step 7: Open the Application in Your Web Browser
- **Web Application Portal:** [http://127.0.0.1:5000](http://127.0.0.1:5000)
- **API Health Endpoint:** [http://127.0.0.1:5000/api/health](http://127.0.0.1:5000/api/health)

---

## 3. Pre-Configured Demo User Credentials

The database comes pre-seeded with ready-to-use accounts for all roles. You can also click the quick-login buttons on the homepage or login screen.

| Role | Name | Email Address | Password | Permissions & Portals |
| :--- | :--- | :--- | :--- | :--- |
| **Patient** | Alice Johnson | `patient.alice@medicare.local` | `PatientPassword123!` | Book appointments, track digital queue ticket, view ML wait times, medical records |
| **Patient** | Bob Williams | `patient.bob@medicare.local` | `PatientPassword123!` | Active waiting patient in queue |
| **Patient** | Clara Oswald | `patient.clara@medicare.local` | `PatientPassword123!` | Patient with completed consultation history |
| **Doctor** | Dr. John Smith | `doctor.smith@medicare.local` | `DoctorPassword123!` | General Medicine: Call next patient, view queue, complete visits & enter notes |
| **Doctor** | Dr. Priya Patel | `doctor.patel@medicare.local` | `DoctorPassword123!` | Pediatrics: Schedule & queue management |
| **Doctor** | Dr. Wei Chen | `doctor.chen@medicare.local` | `DoctorPassword123!` | Cardiology: Schedule & queue management |
| **Doctor** | Dr. Sarah Davis | `doctor.davis@medicare.local` | `DoctorPassword123!` | Dermatology: Schedule & queue management |
| **Doctor** | Dr. Robert Miller | `doctor.miller@medicare.local` | `DoctorPassword123!` | Orthopedics: Schedule & queue management |
| **Admin** | Clinic Administrator | `admin@medicare.local` | `AdminPassword123!` | Full control: Analytics charts, doctors roster, departments CRUD, user management |

---

## 4. In-Depth Feature Documentation

### 4.1 Authentication & Role-Based Access Control (RBAC)
- **Password Security:** Salted SHA-256 password hashing using Werkzeug Security.
- **Stateless Tokens:** JWT tokens signed with HMAC-SHA256 (`Flask-JWT-Extended`) storing `identity`, `role`, `name`, and `email`.
- **Role Decorators:** Route-level `@role_required(['admin', 'doctor', 'patient'])` security protecting unauthorized endpoints.
- **Frontend Guard:** Client-side route interception automatically redirecting unauthorized or expired sessions to `/login`.

### 4.2 Patient Portal Features
- **Dynamic Slot Booking:** Real-time generation of 15-minute appointment slots based on the doctor's weekly calendar and existing bookings.
- **Collision Prevention:** Instant server-side validation rejecting conflicting bookings for the same doctor at the same datetime (HTTP 409).
- **Sequential Daily Token Generation:** Automatic token format `T-{doctor_id:02d}-{count:03d}` (e.g. `T-01-001`, `T-01-002`).
- **Digital Queue Ticket:** Real-time visual ticket showing token number, current queue position, patients ahead, and ML estimated wait time in minutes.
- **Appointment Management:** View upcoming and past appointments with cancellation actions.
- **Medical Records:** Access clinical visit notes, diagnosis labels, and follow-up consultation dates.

### 4.3 Doctor Portal Features
- **Daily Queue Management:** View today's active queue ordered by position and token number.
- **One-Click Call Next Patient:** Automatically advances the queue: marks the previous patient as `COMPLETED` and advances the next waiting patient to `CALLED` / `IN_PROGRESS`.
- **Clinical Consultation Notes Modal:** Record demo diagnosis labels, observations, and prescription advice upon visit completion.
- **No-Show Handling:** Transition patients who fail to arrive to `NO_SHOW` and remove them from the active queue.
- **Schedule Overview:** Filter daily appointments by date.

### 4.4 Clinic Administrator Features
- **Operational Analytics Dashboard:** Live KPI cards for Total Appointments, Completed Visits, Active Queue Load, and Average Waiting Time.
- **Chart.js Visualizations:**
  1. *Appointment Volume Trends:* Line chart tracking total vs. completed visits over time.
  2. *Department Distribution:* Doughnut chart showing appointment demand across specialties.
  3. *Waiting Time Trends:* Bar chart showing average waiting times by specialty.
- **Doctor Directory:** View all doctors, specialties, consultation times, and toggle availability.
- **Department CRUD:** Create, view, update, and delete clinic departments.
- **User Account Directory:** Filter users by role and toggle account activation status (`is_active`).

---

## 5. Complete REST API Specification

Base URL: `/api`  
All protected endpoints require the HTTP header:  
`Authorization: Bearer <access_token>`

### 5.1 Authentication Endpoints

#### `POST /api/auth/register`
Creates a new patient or staff user.
- **Request Body:**
  ```json
  {
    "name": "Jane Doe",
    "email": "jane@example.com",
    "password": "SecurePassword123!",
    "role": "patient",
    "phone": "+1-555-0199",
    "gender": "Female",
    "date_of_birth": "1995-08-20",
    "address": "456 Oak Avenue"
  }
  ```
- **Response (201 Created):**
  ```json
  {
    "success": true,
    "message": "Registration successful",
    "data": {
      "access_token": "eyJhbGci...",
      "user": {
        "id": 10,
        "name": "Jane Doe",
        "email": "jane@example.com",
        "role": "patient",
        "is_active": true
      }
    }
  }
  ```

#### `POST /api/auth/login`
Authenticates user and returns JWT token.
- **Request Body:**
  ```json
  {
    "email": "patient.alice@medicare.local",
    "password": "PatientPassword123!"
  }
  ```
- **Response (200 OK):**
  ```json
  {
    "success": true,
    "message": "Login successful",
    "data": {
      "access_token": "eyJhbGci...",
      "user": {
        "id": 7,
        "name": "Alice Johnson",
        "email": "patient.alice@medicare.local",
        "role": "patient",
        "patient_id": 1
      }
    }
  }
  ```

#### `GET /api/auth/me`
Fetches current logged-in user profile with attached role details.
- **Headers:** `Authorization: Bearer <token>`
- **Response (200 OK):** Returns user object and linked profile.

---

### 5.2 Department Endpoints

#### `GET /api/departments`
Lists all medical departments with doctor counts.
- **Response (200 OK):**
  ```json
  {
    "success": true,
    "data": [
      {
        "id": 1,
        "name": "General Medicine",
        "description": "Primary care and routine general health checkups.",
        "doctor_count": 1
      }
    ]
  }
  ```

#### `POST /api/departments` *(Admin Only)*
Creates a new department.
- **Request Body:**
  ```json
  {
    "name": "Neurology",
    "description": "Brain and nervous system diagnostics and treatments."
  }
  ```

---

### 5.3 Doctor Endpoints

#### `GET /api/doctors`
Lists active doctors. Optional query parameter: `?department_id=1`.

#### `GET /api/doctors/<id>`
Returns doctor profile and weekly schedules.

#### `GET /api/doctors/<id>/availability?date=YYYY-MM-DD`
Computes all available non-conflicting time slots for a given date.
- **Response (200 OK):**
  ```json
  {
    "success": true,
    "data": {
      "doctor_id": 1,
      "doctor_name": "Dr. John Smith",
      "date": "2026-10-05",
      "slot_count": 31,
      "available_slots": ["09:00", "09:15", "09:30", "09:45", "11:00", "..."]
    }
  }
  ```

#### `GET /api/doctors/<id>/queue?date=YYYY-MM-DD`
Retrieves live queue for a doctor on a specific date, including current active patient.

---

### 5.4 Appointment Endpoints

#### `POST /api/appointments`
Books an appointment.
- **Request Body:**
  ```json
  {
    "doctor_id": 1,
    "appointment_date": "2026-10-05",
    "appointment_time": "11:15",
    "reason": "Persistent migraine and dizziness"
  }
  ```
- **Response (201 Created):**
  ```json
  {
    "success": true,
    "message": "Appointment booked successfully",
    "data": {
      "id": 12,
      "token_number": "T-01-004",
      "status": "BOOKED",
      "appointment_date": "2026-10-05",
      "appointment_time": "11:15",
      "queue_position": 4,
      "patients_ahead": 3,
      "estimated_wait_minutes": 45
    }
  }
  ```
- **Error Response (409 Conflict):**
  ```json
  {
    "success": false,
    "error": {
      "code": "APPOINTMENT_CONFLICT",
      "message": "The selected slot is already booked. Please choose another time."
    }
  }
  ```

#### `DELETE /api/appointments/<id>`
Cancels an appointment and automatically triggers real-time queue recalculation for other waiting patients.

---

### 5.5 Digital Queue Endpoints

#### `GET /api/queue/<appointment_id>`
Returns queue position, status, patients ahead, and estimated wait.

#### `POST /api/queue/doctor/<doctor_id>/next` *(Doctor / Admin)*
Calls the next patient in line.
- **Response (200 OK):**
  ```json
  {
    "success": true,
    "message": "Called next patient: Token T-01-001",
    "data": {
      "id": 1,
      "token_number": "T-01-001",
      "patient_name": "Alice Johnson",
      "status": "IN_PROGRESS",
      "queue_status": "CALLED"
    }
  }
  ```

#### `PUT /api/queue/<appointment_id>/status`
Updates queue status (`WAITING`, `CALLED`, `IN_PROGRESS`, `COMPLETED`, `SKIPPED`).

---

### 5.6 Medical Visit Records Endpoints

#### `POST /api/records` *(Doctor / Admin)*
Saves consultation notes and finishes the appointment.
- **Request Body:**
  ```json
  {
    "appointment_id": 1,
    "diagnosis_demo": "Seasonal Allergic Rhinitis (Demo)",
    "notes": "Prescribed antihistamines for 5 days. Recommended air purifier.",
    "follow_up_date": "2026-10-20"
  }
  ```

---

### 5.7 Machine Learning Prediction Endpoints

#### `POST /api/predictions/waiting-time`
Inference endpoint that executes the trained ML Gradient Boosting Regressor model.
- **Request Body:**
  ```json
  {
    "doctor_id": 1,
    "department_id": 1,
    "day_of_week": 2,
    "appointment_hour": 10,
    "patients_ahead": 4,
    "queue_length": 6,
    "average_consultation_time": 15.0
  }
  ```
- **Response (200 OK):**
  ```json
  {
    "success": true,
    "data": {
      "estimated_wait_minutes": 55.8,
      "method": "ml_prediction",
      "model_name": "Gradient Boosting",
      "model_version": "v1.0"
    }
  }
  ```

---

### 5.8 Operational Analytics Endpoints

#### `GET /api/analytics/overview`
Returns high-level operational KPIs.
- **Response (200 OK):**
  ```json
  {
    "success": true,
    "data": {
      "total_appointments": 8,
      "completed_appointments": 5,
      "cancelled_appointments": 0,
      "active_in_queue": 3,
      "average_wait_minutes": 19.7,
      "total_doctors": 5,
      "total_departments": 5
    }
  }
  ```

#### `GET /api/analytics/appointments?days=14`
Daily trends of total vs. completed appointments.

#### `GET /api/analytics/departments`
Distribution of visits across medical specialties.

#### `GET /api/analytics/waiting-times`
Specialty-level average waiting times.

---

## 6. Database Schema & Data Models

MediCare implements a normalized relational database design with foreign key constraints, indexes, and cascading behavior.

```text
┌──────────────┐         ┌──────────────┐         ┌────────────────────┐
│    users     │────────<│   patients   │────────<│  medical_records   │
└──────┬───────┘         └──────┬───────┘         └────────────────────┘
       │                        │                            ▲
       │                        ▼                            │
       │                 ┌──────────────┐                    │
       │                 │ appointments │────────────────────┤
       │                 └──────┬───────┘                    │
       │                        │                            ▼
       ▼                        ├─────────────────>┌────────────────────┐
┌──────────────┐                │                  │   queue_records    │
│   doctors    │────────────────┤                  └────────────────────┘
└──────┬───────┘                │                            ▲
       │                        ▼                            │
       ├───────────────> ┌──────────────┐                    │
       │                 │prediction_log│────────────────────┘
       ▼                 └──────────────┘
┌──────────────┐
│ departments  │
└──────────────┘
```

### Table Definitions
1. **`users`**: `id`, `name`, `email` (unique index), `password_hash`, `role` (`patient`, `doctor`, `admin`), `is_active`, `created_at`, `updated_at`.
2. **`patients`**: `id`, `user_id` (FK `users.id`), `date_of_birth`, `gender`, `phone`, `address`, `created_at`, `updated_at`.
3. **`doctors`**: `id`, `user_id` (FK `users.id`), `department_id` (FK `departments.id`), `specialization`, `experience_years`, `consultation_duration_minutes`, `is_available`, `created_at`.
4. **`departments`**: `id`, `name` (unique), `description`, `created_at`.
5. **`doctor_schedules`**: `id`, `doctor_id` (FK `doctors.id`), `day_of_week` (0=Mon...6=Sun), `start_time`, `end_time`, `slot_duration_minutes`, `max_appointments`.
6. **`appointments`**: `id`, `patient_id` (FK `patients.id`), `doctor_id` (FK `doctors.id`), `appointment_date`, `appointment_time`, `token_number`, `status` (`BOOKED`, `CONFIRMED`, `WAITING`, `IN_PROGRESS`, `COMPLETED`, `CANCELLED`, `NO_SHOW`), `reason`, `created_at`. Unique constraint: `(doctor_id, appointment_date, appointment_time)`.
7. **`queue_records`**: `id`, `appointment_id` (FK `appointments.id`, unique), `doctor_id` (FK `doctors.id`), `queue_position`, `patients_ahead`, `estimated_wait_minutes`, `queue_status` (`WAITING`, `CALLED`, `IN_PROGRESS`, `COMPLETED`, `SKIPPED`).
8. **`medical_records`**: `id`, `patient_id` (FK `patients.id`), `doctor_id` (FK `doctors.id`), `appointment_id` (FK `appointments.id`, unique), `visit_date`, `diagnosis_demo`, `notes`, `follow_up_date`.
9. **`prediction_logs`**: `id`, `appointment_id` (FK `appointments.id`), `model_version`, `predicted_wait_minutes`, `actual_wait_minutes`, `prediction_created_at`.

---

## 7. Machine Learning Pipeline & Evaluation

### Feature Engineering
The waiting time estimation pipeline models real hospital dynamics using the following features:
- `doctor_id`: Physician identifier
- `department_id`: Medical specialty identifier
- `day_of_week`: Day index (Mondays and Fridays exhibit surge factors)
- `appointment_hour`: Time of day (rush hours at 10-12 AM and 4-5 PM)
- `patients_ahead`: Number of active waiting patients ahead of the current token
- `queue_length`: Total active queue length for the doctor
- `average_consultation_time`: Average duration per patient (10 to 20 minutes)
- `appointments_scheduled`: Total volume scheduled on that day
- `historical_average_wait`: Rolling baseline wait time

### Model Comparison & Measured Results
Three candidate regressors were trained on an 80/20 train/test split:

| Model Candidate | Mean Absolute Error (MAE) | Root Mean Squared Error (RMSE) | R² Score | Status |
| :--- | :---: | :---: | :---: | :---: |
| **Linear Regression** | 11.72 mins | 15.42 mins | 0.9344 | Baseline |
| **Random Forest Regressor** | 3.79 mins | 5.57 mins | 0.9915 | Candidate |
| **Gradient Boosting Regressor** | **3.45 mins** | **4.75 mins** | **0.9938** | **Selected Best Model** |

The **Gradient Boosting Regressor** was selected as the optimal model based on lowest prediction error (MAE: 3.45 min) and serialized to `ml/model.joblib`.

---

## 8. Automated Testing Guide

MediCare includes a comprehensive automated test suite built with `pytest`.

### Running All Tests
```powershell
pytest
```

### Test Coverage Summary (15 Passed Tests)
- `tests/test_auth.py`:
  - `test_health_check`: Verifies API health and version.
  - `test_register_patient_success`: Verifies patient registration and JWT creation.
  - `test_register_duplicate_email`: Ensures duplicate emails are rejected with HTTP 409.
  - `test_login_success`: Verifies valid credential authentication.
  - `test_login_invalid_password`: Verifies invalid password rejection.
  - `test_me_protected_endpoint`: Verifies token-protected profile retrieval.
- `tests/test_appointments.py`:
  - `test_get_doctor_availability`: Checks slot generation based on doctor schedule.
  - `test_book_appointment_success`: Verifies booking and token generation (`T-01-xxx`).
  - `test_book_duplicate_appointment_conflict`: Tests strict conflict rejection on duplicate slot booking.
  - `test_cancel_appointment`: Tests patient cancellation and queue recalculation.
- `tests/test_queue.py`:
  - `test_queue_flow`: Tests appointment-to-queue mapping and doctor advancing queue tickets.
- `tests/test_ml.py`:
  - `test_ml_prediction_endpoint`: Verifies feature validation and positive wait time return.
  - `test_ml_zero_patients_ahead`: Verifies zero wait time when no patients are ahead.
- `tests/test_analytics.py`:
  - `test_analytics_overview`: Verifies KPI metrics structure.
  - `test_analytics_departments`: Verifies department distribution data.

---

## 9. Docker Deployment

To run the complete application using Docker and Docker Compose:

### 1. Build and Run Containers
```bash
docker-compose up --build
```

### 2. Access the Application
Open [http://localhost:5000](http://localhost:5000) in your web browser.

---

## 10. Security & Educational Disclaimer

- **Educational & Portfolio Scope:** MediCare is designed for demonstration and educational purposes. It utilizes synthetic, non-clinical data and should **not** be used for real emergency medical services or storing real protected health information (PHI).
- **Security Best Practices:** Environment-based secrets management, parameterized SQL via SQLAlchemy, role-based authorization headers, and input sanitization are implemented throughout the codebase.
