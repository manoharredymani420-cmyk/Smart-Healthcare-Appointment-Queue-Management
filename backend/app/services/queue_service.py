from datetime import datetime, timezone
from backend.app.extensions import db
from backend.app.models.appointment import Appointment
from backend.app.models.queue import QueueRecord
from backend.app.models.doctor import Doctor
from backend.app.services.prediction_service import predict_wait_time

def recalculate_doctor_queue(doctor_id: int, target_date):
    """
    Recalculates queue positions, patients_ahead, and estimated wait times
    for all active waiting appointments for a specific doctor and date.
    """
    # Active waiting appointments ordered by appointment_time, token_number
    active_appointments = (
        Appointment.query
        .filter(
            Appointment.doctor_id == doctor_id,
            Appointment.appointment_date == target_date,
            Appointment.status.in_(['BOOKED', 'CONFIRMED', 'WAITING'])
        )
        .order_by(Appointment.appointment_time.asc(), Appointment.id.asc())
        .all()
    )

    doctor = db.session.get(Doctor, doctor_id)
    consultation_time = doctor.consultation_duration_minutes if doctor else 15
    department_id = doctor.department_id if doctor and doctor.department_id else 1
    total_active = len(active_appointments)

    for index, appt in enumerate(active_appointments):
        position = index + 1
        patients_ahead = index
        
        # Calculate predicted wait time
        day_of_week = target_date.weekday()
        appointment_hour = appt.appointment_time.hour if appt.appointment_time else 10
        
        pred_result = predict_wait_time(
            doctor_id=doctor_id,
            department_id=department_id,
            day_of_week=day_of_week,
            appointment_hour=appointment_hour,
            patients_ahead=patients_ahead,
            queue_length=total_active,
            average_consultation_time=float(consultation_time)
        )
        estimated_wait = int(round(pred_result['estimated_wait_minutes']))

        if not appt.queue_record:
            q_rec = QueueRecord(
                appointment_id=appt.id,
                doctor_id=doctor_id,
                queue_position=position,
                patients_ahead=patients_ahead,
                estimated_wait_minutes=estimated_wait,
                queue_status='WAITING'
            )
            db.session.add(q_rec)
        else:
            appt.queue_record.queue_position = position
            appt.queue_record.patients_ahead = patients_ahead
            appt.queue_record.estimated_wait_minutes = estimated_wait
            if appt.queue_record.queue_status not in ['CALLED', 'IN_PROGRESS']:
                appt.queue_record.queue_status = 'WAITING'

    db.session.commit()

def call_next_patient(doctor_id: int, target_date=None):
    """
    Advances the queue for a doctor:
    1. If a patient is currently IN_PROGRESS or CALLED, they are marked COMPLETED.
    2. The first WAITING patient is transitioned to CALLED / IN_PROGRESS.
    """
    if target_date is None:
        target_date = datetime.now(timezone.utc).date()

    # Find currently active patient (CALLED or IN_PROGRESS)
    current_active = (
        Appointment.query
        .join(QueueRecord)
        .filter(
            Appointment.doctor_id == doctor_id,
            Appointment.appointment_date == target_date,
            Appointment.status.in_(['WAITING', 'IN_PROGRESS']),
            QueueRecord.queue_status.in_(['CALLED', 'IN_PROGRESS'])
        )
        .first()
    )

    if current_active:
        current_active.status = 'COMPLETED'
        if current_active.queue_record:
            current_active.queue_record.queue_status = 'COMPLETED'
            current_active.queue_record.estimated_wait_minutes = 0

    # Next patient in line
    next_patient_appt = (
        Appointment.query
        .join(QueueRecord)
        .filter(
            Appointment.doctor_id == doctor_id,
            Appointment.appointment_date == target_date,
            Appointment.status.in_(['BOOKED', 'CONFIRMED', 'WAITING']),
            QueueRecord.queue_status == 'WAITING'
        )
        .order_by(QueueRecord.queue_position.asc())
        .first()
    )

    if next_patient_appt:
        next_patient_appt.status = 'IN_PROGRESS'
        next_patient_appt.queue_record.queue_status = 'CALLED'
        next_patient_appt.queue_record.patients_ahead = 0
        next_patient_appt.queue_record.estimated_wait_minutes = 0

    db.session.commit()
    recalculate_doctor_queue(doctor_id, target_date)
    return next_patient_appt
