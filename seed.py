import os
from datetime import datetime, date, time, timedelta, timezone
from backend.app import create_app
from backend.app.extensions import db
from backend.app.models import (
    User, Patient, Doctor, Department, DoctorSchedule,
    Appointment, QueueRecord, MedicalRecord, PredictionLog
)
from backend.app.utils.security import hash_password
from backend.app.services.queue_service import recalculate_doctor_queue

def seed_database():
    app = create_app('development')
    with app.app_context():
        print("Resetting and initializing database...")
        db.drop_all()
        db.create_all()

        print("1. Seeding Departments...")
        departments_data = [
            {"name": "General Medicine", "description": "Primary care and routine general health checkups."},
            {"name": "Pediatrics", "description": "Comprehensive medical care for infants, children, and adolescents."},
            {"name": "Dermatology", "description": "Skin, hair, and nail diagnosis and treatments."},
            {"name": "Orthopedics", "description": "Musculoskeletal system, bone, and joint care."},
            {"name": "Cardiology", "description": "Heart disease prevention, diagnosis, and cardiovascular health."}
        ]
        dept_objs = {}
        for d in departments_data:
            dept = Department(name=d["name"], description=d["description"])
            db.session.add(dept)
            db.session.flush()
            dept_objs[d["name"]] = dept

        print("2. Seeding Admin...")
        admin = User(
            name="Clinic Administrator",
            email="admin@medicare.local",
            password_hash=hash_password("AdminPassword123!"),
            role="admin"
        )
        db.session.add(admin)

        print("3. Seeding Doctors...")
        doctors_info = [
            {"name": "Dr. John Smith", "email": "doctor.smith@medicare.local", "dept": "General Medicine", "spec": "Internal Medicine", "exp": 12, "dur": 15},
            {"name": "Dr. Priya Patel", "email": "doctor.patel@medicare.local", "dept": "Pediatrics", "spec": "Pediatrician", "exp": 8, "dur": 15},
            {"name": "Dr. Wei Chen", "email": "doctor.chen@medicare.local", "dept": "Cardiology", "spec": "Cardiologist", "exp": 15, "dur": 20},
            {"name": "Dr. Sarah Davis", "email": "doctor.davis@medicare.local", "dept": "Dermatology", "spec": "Dermatologist", "exp": 6, "dur": 12},
            {"name": "Dr. Robert Miller", "email": "doctor.miller@medicare.local", "dept": "Orthopedics", "spec": "Orthopedic Surgeon", "exp": 14, "dur": 18}
        ]
        doctor_objs = []
        for doc in doctors_info:
            user = User(
                name=doc["name"],
                email=doc["email"],
                password_hash=hash_password("DoctorPassword123!"),
                role="doctor"
            )
            db.session.add(user)
            db.session.flush()

            doctor_record = Doctor(
                user_id=user.id,
                department_id=dept_objs[doc["dept"]].id,
                specialization=doc["spec"],
                experience_years=doc["exp"],
                consultation_duration_minutes=doc["dur"],
                is_available=True
            )
            db.session.add(doctor_record)
            db.session.flush()
            doctor_objs.append(doctor_record)

            # Add weekly schedules (Monday to Friday, 09:00 - 17:00)
            for day in range(5):
                sched = DoctorSchedule(
                    doctor_id=doctor_record.id,
                    day_of_week=day,
                    start_time=time(9, 0),
                    end_time=time(17, 0),
                    slot_duration_minutes=doc["dur"],
                    max_appointments=25
                )
                db.session.add(sched)

        print("4. Seeding Patients...")
        patients_info = [
            {"name": "Alice Johnson", "email": "patient.alice@medicare.local", "dob": "1994-05-12", "gender": "Female", "phone": "+1-555-0101", "address": "124 Pine Street"},
            {"name": "Bob Williams", "email": "patient.bob@medicare.local", "dob": "1988-11-23", "gender": "Male", "phone": "+1-555-0102", "address": "742 Evergreen Terrace"},
            {"name": "Clara Oswald", "email": "patient.clara@medicare.local", "dob": "1996-03-08", "gender": "Female", "phone": "+1-555-0103", "address": "42 Market Street"},
            {"name": "David Miller", "email": "patient.david@medicare.local", "dob": "1975-09-17", "gender": "Male", "phone": "+1-555-0104", "address": "88 Elm Drive"}
        ]
        patient_objs = []
        for pat in patients_info:
            user = User(
                name=pat["name"],
                email=pat["email"],
                password_hash=hash_password("PatientPassword123!"),
                role="patient"
            )
            db.session.add(user)
            db.session.flush()

            patient_record = Patient(
                user_id=user.id,
                date_of_birth=datetime.strptime(pat["dob"], "%Y-%m-%d").date(),
                gender=pat["gender"],
                phone=pat["phone"],
                address=pat["address"]
            )
            db.session.add(patient_record)
            db.session.flush()
            patient_objs.append(patient_record)

        print("5. Seeding Appointments & Queue...")
        today = datetime.now(timezone.utc).date()
        doc_smith = doctor_objs[0]  # Dr. John Smith

        # Today's queue for Dr. Smith
        # 1. Alice Johnson (Waiting, Token T-01-001)
        appt1 = Appointment(
            patient_id=patient_objs[0].id,
            doctor_id=doc_smith.id,
            appointment_date=today,
            appointment_time=time(10, 0),
            token_number="T-01-001",
            status="WAITING",
            reason="Persistent seasonal cough and throat soreness."
        )
        db.session.add(appt1)
        db.session.flush()

        # 2. Bob Williams (Waiting, Token T-01-002)
        appt2 = Appointment(
            patient_id=patient_objs[1].id,
            doctor_id=doc_smith.id,
            appointment_date=today,
            appointment_time=time(10, 15),
            token_number="T-01-002",
            status="WAITING",
            reason="Annual wellness checkup and blood work discussion."
        )
        db.session.add(appt2)
        db.session.flush()

        # 3. David Miller (Waiting, Token T-01-003)
        appt3 = Appointment(
            patient_id=patient_objs[3].id,
            doctor_id=doc_smith.id,
            appointment_date=today,
            appointment_time=time(10, 30),
            token_number="T-01-003",
            status="WAITING",
            reason="Mild hypertension follow-up."
        )
        db.session.add(appt3)
        db.session.flush()

        # Historical completed appointments for trends & charts
        past_dates = [today - timedelta(days=i) for i in range(1, 6)]
        for idx, p_date in enumerate(past_dates):
            # Completed appt
            completed_appt = Appointment(
                patient_id=patient_objs[idx % len(patient_objs)].id,
                doctor_id=doctor_objs[idx % len(doctor_objs)].id,
                appointment_date=p_date,
                appointment_time=time(9 + (idx % 4), 30),
                token_number=f"T-{doctor_objs[idx % len(doctor_objs)].id:02d}-{idx + 1:03d}",
                status="COMPLETED",
                reason="Routine consultation"
            )
            db.session.add(completed_appt)
            db.session.flush()

            # Add visit record
            med_rec = MedicalRecord(
                patient_id=completed_appt.patient_id,
                doctor_id=completed_appt.doctor_id,
                appointment_id=completed_appt.id,
                visit_date=p_date,
                diagnosis_demo="Upper Respiratory Tract Infection (Demo)",
                notes="Patient advised hydration, rest, and 5-day demo medication regimen.",
                follow_up_date=p_date + timedelta(days=14)
            )
            db.session.add(med_rec)

        db.session.commit()

        # Recalculate queue for today
        recalculate_doctor_queue(doc_smith.id, today)
        print("Database successfully seeded with realistic healthcare clinic data!")

if __name__ == '__main__':
    seed_database()
