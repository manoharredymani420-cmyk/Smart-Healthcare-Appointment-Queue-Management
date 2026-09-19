from datetime import datetime, date, time
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from backend.app.extensions import db
from backend.app.models.doctor import Doctor
from backend.app.models.schedule import DoctorSchedule
from backend.app.models.appointment import Appointment
from backend.app.models.queue import QueueRecord
from backend.app.models.user import User
from backend.app.services.appointment_service import get_doctor_available_slots
from backend.app.utils.decorators import role_required
from backend.app.utils.errors import api_response, api_error

doctors_bp = Blueprint('doctors', __name__, url_prefix='/api/doctors')

@doctors_bp.route('', methods=['GET'])
def list_doctors():
    department_id = request.args.get('department_id', type=int)
    query = Doctor.query.filter_by(is_available=True)
    if department_id:
        query = query.filter_by(department_id=department_id)
    doctors = query.all()
    return api_response([d.to_dict() for d in doctors])

@doctors_bp.route('/<int:doc_id>', methods=['GET'])
def get_doctor(doc_id):
    doctor = db.session.get(Doctor, doc_id)
    if not doctor:
        return api_error("Doctor not found", code="DOCTOR_NOT_FOUND", status_code=404)
    data = doctor.to_dict()
    data['schedules'] = [s.to_dict() for s in doctor.schedules.all()]
    return api_response(data)

@doctors_bp.route('/<int:doc_id>/availability', methods=['GET'])
def doctor_availability(doc_id):
    date_str = request.args.get('date')
    if not date_str:
        return api_error("Date parameter is required (format: YYYY-MM-DD)", code="MISSING_PARAM", status_code=400)
    
    try:
        target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return api_error("Invalid date format, use YYYY-MM-DD", code="INVALID_DATE_FORMAT", status_code=400)

    doctor = db.session.get(Doctor, doc_id)
    if not doctor:
        return api_error("Doctor not found", code="DOCTOR_NOT_FOUND", status_code=404)

    slots = get_doctor_available_slots(doc_id, target_date)
    return api_response({
        'doctor_id': doc_id,
        'doctor_name': doctor.user.name if doctor.user else None,
        'date': target_date.isoformat(),
        'available_slots': slots,
        'slot_count': len(slots)
    })

@doctors_bp.route('/<int:doc_id>/appointments', methods=['GET'])
@role_required(['doctor', 'admin'])
def doctor_appointments(doc_id):
    date_str = request.args.get('date')
    query = Appointment.query.filter_by(doctor_id=doc_id)
    if date_str:
        try:
            target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            query = query.filter_by(appointment_date=target_date)
        except ValueError:
            pass

    appointments = query.order_by(Appointment.appointment_date.desc(), Appointment.appointment_time.asc()).all()
    return api_response([a.to_dict() for a in appointments])

@doctors_bp.route('/<int:doc_id>/queue', methods=['GET'])
def doctor_queue(doc_id):
    date_str = request.args.get('date')
    if date_str:
        try:
            target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            target_date = datetime.now().date()
    else:
        target_date = datetime.now().date()

    appointments = (
        Appointment.query
        .join(QueueRecord)
        .filter(
            Appointment.doctor_id == doc_id,
            Appointment.appointment_date == target_date,
            Appointment.status.in_(['BOOKED', 'CONFIRMED', 'WAITING', 'IN_PROGRESS', 'COMPLETED'])
        )
        .order_by(QueueRecord.queue_position.asc())
        .all()
    )

    queue_list = []
    current_patient = None
    for a in appointments:
        item = a.to_dict()
        if item.get('queue_status') in ['CALLED', 'IN_PROGRESS']:
            current_patient = item
        queue_list.append(item)

    return api_response({
        'doctor_id': doc_id,
        'date': target_date.isoformat(),
        'queue': queue_list,
        'total_in_queue': len([q for q in queue_list if q.get('queue_status') == 'WAITING']),
        'current_patient': current_patient
    })
