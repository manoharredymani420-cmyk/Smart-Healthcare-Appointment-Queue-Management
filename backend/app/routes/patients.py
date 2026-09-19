from datetime import datetime
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.app.extensions import db
from backend.app.models.patient import Patient
from backend.app.models.appointment import Appointment
from backend.app.models.medical_record import MedicalRecord
from backend.app.utils.errors import api_response, api_error

patients_bp = Blueprint('patients', __name__, url_prefix='/api/patients')

@patients_bp.route('/me', methods=['GET'])
@jwt_required()
def get_my_profile():
    user_id = int(get_jwt_identity())
    patient = Patient.query.filter_by(user_id=user_id).first()
    if not patient:
        return api_error("Patient profile not found", code="NOT_FOUND", status_code=404)
    return api_response(patient.to_dict())

@patients_bp.route('/me', methods=['PUT'])
@jwt_required()
def update_my_profile():
    user_id = int(get_jwt_identity())
    patient = Patient.query.filter_by(user_id=user_id).first()
    if not patient:
        return api_error("Patient profile not found", code="NOT_FOUND", status_code=404)

    data = request.get_json() or {}
    if 'phone' in data:
        patient.phone = data['phone'].strip()
    if 'gender' in data:
        patient.gender = data['gender'].strip()
    if 'address' in data:
        patient.address = data['address'].strip()
    if 'date_of_birth' in data and data['date_of_birth']:
        try:
            patient.date_of_birth = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
        except ValueError:
            return api_error("Invalid date_of_birth, format must be YYYY-MM-DD", code="INVALID_DATE", status_code=400)

    db.session.commit()
    return api_response(patient.to_dict(), message="Profile updated successfully")

@patients_bp.route('/me/appointments', methods=['GET'])
@jwt_required()
def get_my_appointments():
    user_id = int(get_jwt_identity())
    patient = Patient.query.filter_by(user_id=user_id).first()
    if not patient:
        return api_error("Patient profile not found", code="NOT_FOUND", status_code=404)

    appointments = (
        Appointment.query
        .filter_by(patient_id=patient.id)
        .order_by(Appointment.appointment_date.desc(), Appointment.appointment_time.asc())
        .all()
    )
    return api_response([a.to_dict() for a in appointments])

@patients_bp.route('/me/records', methods=['GET'])
@jwt_required()
def get_my_records():
    user_id = int(get_jwt_identity())
    patient = Patient.query.filter_by(user_id=user_id).first()
    if not patient:
        return api_error("Patient profile not found", code="NOT_FOUND", status_code=404)

    records = (
        MedicalRecord.query
        .filter_by(patient_id=patient.id)
        .order_by(MedicalRecord.visit_date.desc())
        .all()
    )
    return api_response([r.to_dict() for r in records])
