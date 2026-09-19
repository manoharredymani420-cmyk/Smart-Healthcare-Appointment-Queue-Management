from datetime import datetime
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from backend.app.extensions import db
from backend.app.models.appointment import Appointment
from backend.app.models.patient import Patient
from backend.app.models.doctor import Doctor
from backend.app.services.appointment_service import book_appointment, cancel_appointment
from backend.app.services.queue_service import recalculate_doctor_queue
from backend.app.utils.errors import api_response, api_error

appointments_bp = Blueprint('appointments', __name__, url_prefix='/api/appointments')

@appointments_bp.route('', methods=['GET'])
@jwt_required()
def list_appointments():
    user_id = int(get_jwt_identity())
    claims = get_jwt()
    role = claims.get('role', 'patient')

    date_str = request.args.get('date')
    status = request.args.get('status')
    
    query = Appointment.query

    if role == 'patient':
        patient = Patient.query.filter_by(user_id=user_id).first()
        if not patient:
            return api_error("Patient profile not found", code="NOT_FOUND", status_code=404)
        query = query.filter_by(patient_id=patient.id)
    elif role == 'doctor':
        doctor = Doctor.query.filter_by(user_id=user_id).first()
        if not doctor:
            return api_error("Doctor profile not found", code="NOT_FOUND", status_code=404)
        query = query.filter_by(doctor_id=doctor.id)

    if date_str:
        try:
            target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            query = query.filter_by(appointment_date=target_date)
        except ValueError:
            pass

    if status:
        query = query.filter_by(status=status.upper())

    appointments = query.order_by(Appointment.appointment_date.desc(), Appointment.appointment_time.asc()).all()
    return api_response([a.to_dict() for a in appointments])

@appointments_bp.route('', methods=['POST'])
@jwt_required()
def create_appointment():
    user_id = int(get_jwt_identity())
    claims = get_jwt()
    role = claims.get('role', 'patient')
    data = request.get_json() or {}

    doctor_id = data.get('doctor_id')
    date_str = data.get('appointment_date')
    time_str = data.get('appointment_time')
    reason = data.get('reason', '').strip()

    if not doctor_id or not date_str or not time_str:
        return api_error("doctor_id, appointment_date, and appointment_time are required", 
                         code="VALIDATION_ERROR", status_code=400)

    try:
        appt_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return api_error("Invalid appointment_date, format must be YYYY-MM-DD", 
                         code="INVALID_DATE_FORMAT", status_code=400)

    try:
        # Support formats HH:MM or HH:MM:SS
        if len(time_str.split(':')) == 2:
            appt_time = datetime.strptime(time_str, '%H:%M').time()
        else:
            appt_time = datetime.strptime(time_str, '%H:%M:%S').time()
    except ValueError:
        return api_error("Invalid appointment_time, format must be HH:MM", 
                         code="INVALID_TIME_FORMAT", status_code=400)

    # Determine patient_id
    if role == 'patient':
        patient = Patient.query.filter_by(user_id=user_id).first()
        if not patient:
            return api_error("Patient profile not found", code="PATIENT_NOT_FOUND", status_code=404)
        patient_id = patient.id
    elif role in ['admin', 'doctor']:
        patient_id = data.get('patient_id')
        if not patient_id:
            return api_error("patient_id is required for staff booking", code="VALIDATION_ERROR", status_code=400)
    else:
        return api_error("Unauthorized to book appointment", code="UNAUTHORIZED", status_code=403)

    try:
        appointment = book_appointment(
            patient_id=patient_id,
            doctor_id=doctor_id,
            appt_date=appt_date,
            appt_time=appt_time,
            reason=reason
        )
        return api_response(appointment.to_dict(), message="Appointment booked successfully", status_code=201)
    except ValueError as e:
        return api_error(str(e), code="APPOINTMENT_CONFLICT", status_code=409)
    except Exception as e:
        return api_error(f"Failed to book appointment: {str(e)}", code="BOOKING_ERROR", status_code=500)

@appointments_bp.route('/<int:appt_id>', methods=['GET'])
@jwt_required()
def get_appointment(appt_id):
    appointment = db.session.get(Appointment, appt_id)
    if not appointment:
        return api_error("Appointment not found", code="APPOINTMENT_NOT_FOUND", status_code=404)
    return api_response(appointment.to_dict())

@appointments_bp.route('/<int:appt_id>', methods=['PUT'])
@jwt_required()
def update_appointment(appt_id):
    appointment = db.session.get(Appointment, appt_id)
    if not appointment:
        return api_error("Appointment not found", code="APPOINTMENT_NOT_FOUND", status_code=404)

    data = request.get_json() or {}
    new_status = data.get('status')
    valid_statuses = ['BOOKED', 'CONFIRMED', 'WAITING', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED', 'NO_SHOW']

    if new_status:
        new_status = new_status.upper()
        if new_status not in valid_statuses:
            return api_error(f"Invalid status. Must be one of: {', '.join(valid_statuses)}", 
                             code="INVALID_STATUS", status_code=400)
        appointment.status = new_status
        if appointment.queue_record:
            if new_status == 'COMPLETED':
                appointment.queue_record.queue_status = 'COMPLETED'
                appointment.queue_record.estimated_wait_minutes = 0
            elif new_status in ['CANCELLED', 'NO_SHOW']:
                appointment.queue_record.queue_status = 'SKIPPED'
                appointment.queue_record.estimated_wait_minutes = 0

    if 'reason' in data:
        appointment.reason = data['reason'].strip()

    db.session.commit()
    recalculate_doctor_queue(appointment.doctor_id, appointment.appointment_date)
    return api_response(appointment.to_dict(), message="Appointment updated successfully")

@appointments_bp.route('/<int:appt_id>', methods=['DELETE'])
@jwt_required()
def delete_appointment(appt_id):
    user_id = int(get_jwt_identity())
    claims = get_jwt()
    role = claims.get('role', 'patient')

    try:
        cancelled = cancel_appointment(appt_id, user_id, role)
        return api_response(cancelled.to_dict(), message="Appointment cancelled successfully")
    except ValueError as e:
        return api_error(str(e), code="CANCEL_ERROR", status_code=400)
    except PermissionError as e:
        return api_error(str(e), code="FORBIDDEN", status_code=403)
    except Exception as e:
        return api_error(f"Error cancelling appointment: {str(e)}", code="SERVER_ERROR", status_code=500)
