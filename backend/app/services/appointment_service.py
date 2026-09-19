from datetime import datetime, date, time, timedelta, timezone
from backend.app.extensions import db
from backend.app.models.appointment import Appointment
from backend.app.models.doctor import Doctor
from backend.app.models.schedule import DoctorSchedule
from backend.app.models.queue import QueueRecord
from backend.app.services.queue_service import recalculate_doctor_queue

def get_doctor_available_slots(doctor_id: int, target_date: date):
    """
    Computes all available time slots for a doctor on a specific date.
    Considers the doctor's weekly schedule and excludes existing non-cancelled bookings.
    """
    doctor = db.session.get(Doctor, doctor_id)
    if not doctor or not doctor.is_available:
        return []

    day_of_week = target_date.weekday()  # 0=Monday, 6=Sunday
    schedule = DoctorSchedule.query.filter_by(doctor_id=doctor_id, day_of_week=day_of_week).first()
    
    # If no custom schedule, default to 09:00 - 17:00 Monday to Friday
    if not schedule:
        if day_of_week in [5, 6]:  # Weekend closed if not in schedule
            return []
        start_t = time(9, 0)
        end_t = time(17, 0)
        duration = doctor.consultation_duration_minutes or 15
    else:
        start_t = schedule.start_time
        end_t = schedule.end_time
        duration = schedule.slot_duration_minutes or doctor.consultation_duration_minutes or 15

    # Generate all candidate slots
    slots = []
    current_dt = datetime.combine(target_date, start_t)
    end_dt = datetime.combine(target_date, end_t)
    
    while current_dt + timedelta(minutes=duration) <= end_dt:
        slots.append(current_dt.time())
        current_dt += timedelta(minutes=duration)

    # Fetch existing active bookings for this doctor on target_date
    booked_appointments = (
        Appointment.query
        .filter(
            Appointment.doctor_id == doctor_id,
            Appointment.appointment_date == target_date,
            Appointment.status.notin_(['CANCELLED'])
        )
        .all()
    )
    booked_times = {appt.appointment_time for appt in booked_appointments}

    available_slots = [
        s.strftime('%H:%M') for s in slots if s not in booked_times
    ]
    return available_slots

def book_appointment(patient_id: int, doctor_id: int, appt_date: date, appt_time: time, reason: str = None):
    """
    Books an appointment ensuring no conflict exists for the doctor at that datetime.
    Generates token number and queue record.
    """
    doctor = db.session.get(Doctor, doctor_id)
    if not doctor:
        raise ValueError("Doctor not found")
    if not doctor.is_available:
        raise ValueError("Doctor is currently unavailable")

    # Check for slot conflict
    existing = Appointment.query.filter(
        Appointment.doctor_id == doctor_id,
        Appointment.appointment_date == appt_date,
        Appointment.appointment_time == appt_time,
        Appointment.status.notin_(['CANCELLED'])
    ).first()

    if existing:
        raise ValueError("The selected slot is already booked. Please choose another time.")

    # Generate token number for this doctor on this day
    day_count = Appointment.query.filter(
        Appointment.doctor_id == doctor_id,
        Appointment.appointment_date == appt_date
    ).count()
    token_number = f"T-{doctor_id:02d}-{day_count + 1:03d}"

    appointment = Appointment(
        patient_id=patient_id,
        doctor_id=doctor_id,
        appointment_date=appt_date,
        appointment_time=appt_time,
        token_number=token_number,
        status='BOOKED',
        reason=reason
    )
    db.session.add(appointment)
    db.session.flush()

    # Create Initial Queue Record
    queue_record = QueueRecord(
        appointment_id=appointment.id,
        doctor_id=doctor_id,
        queue_position=day_count + 1,
        patients_ahead=day_count,
        estimated_wait_minutes=(day_count * (doctor.consultation_duration_minutes or 15)),
        queue_status='WAITING'
    )
    db.session.add(queue_record)
    db.session.commit()

    # Recalculate queue with ML estimation
    recalculate_doctor_queue(doctor_id, appt_date)

    return appointment

def cancel_appointment(appointment_id: int, user_id: int, user_role: str):
    """
    Cancels an appointment and updates queue positions for other patients.
    """
    appointment = db.session.get(Appointment, appointment_id)
    if not appointment:
        raise ValueError("Appointment not found")

    # Role permission check
    if user_role == 'patient' and appointment.patient.user_id != user_id:
        raise PermissionError("You are not authorized to cancel this appointment")
    if user_role == 'doctor' and appointment.doctor.user_id != user_id:
        raise PermissionError("You are not authorized to cancel this appointment")

    if appointment.status in ['COMPLETED', 'CANCELLED']:
        raise ValueError(f"Cannot cancel appointment with status '{appointment.status}'")

    appointment.status = 'CANCELLED'
    if appointment.queue_record:
        appointment.queue_record.queue_status = 'SKIPPED'
        appointment.queue_record.estimated_wait_minutes = 0

    db.session.commit()

    # Recalculate remaining queue
    recalculate_doctor_queue(appointment.doctor_id, appointment.appointment_date)
    return appointment
