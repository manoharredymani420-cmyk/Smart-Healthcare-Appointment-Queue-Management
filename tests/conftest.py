import pytest
from datetime import datetime, date, time, timezone
from backend.app import create_app
from backend.app.extensions import db
from backend.app.models import User, Patient, Doctor, Department, DoctorSchedule, Appointment, QueueRecord
from backend.app.utils.security import hash_password
from flask_jwt_extended import create_access_token

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()

        # Seed minimal fixtures
        dept = Department(name="General Medicine", description="General care")
        db.session.add(dept)
        db.session.flush()

        # Admin
        admin_u = User(name="Admin User", email="admin@test.com", password_hash=hash_password("Pass123!"), role="admin")
        db.session.add(admin_u)

        # Doctor
        doc_u = User(name="Dr. Tester", email="doctor@test.com", password_hash=hash_password("Pass123!"), role="doctor")
        db.session.add(doc_u)
        db.session.flush()

        doctor = Doctor(
            user_id=doc_u.id,
            department_id=dept.id,
            specialization="General Physician",
            experience_years=5,
            consultation_duration_minutes=15,
            is_available=True
        )
        db.session.add(doctor)
        db.session.flush()

        # Schedule for Doctor (Monday to Friday)
        for day in range(5):
            sched = DoctorSchedule(
                doctor_id=doctor.id,
                day_of_week=day,
                start_time=time(9, 0),
                end_time=time(17, 0),
                slot_duration_minutes=15
            )
            db.session.add(sched)

        # Patient
        pat_u = User(name="Patient Tester", email="patient@test.com", password_hash=hash_password("Pass123!"), role="patient")
        db.session.add(pat_u)
        db.session.flush()

        patient = Patient(user_id=pat_u.id, phone="555-1234", gender="Other")
        db.session.add(patient)

        db.session.commit()

        yield app

        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def patient_token(app):
    with app.app_context():
        user = User.query.filter_by(email="patient@test.com").first()
        return create_access_token(identity=str(user.id), additional_claims={'role': user.role, 'name': user.name})

@pytest.fixture
def doctor_token(app):
    with app.app_context():
        user = User.query.filter_by(email="doctor@test.com").first()
        return create_access_token(identity=str(user.id), additional_claims={'role': user.role, 'name': user.name})

@pytest.fixture
def admin_token(app):
    with app.app_context():
        user = User.query.filter_by(email="admin@test.com").first()
        return create_access_token(identity=str(user.id), additional_claims={'role': user.role, 'name': user.name})
