from datetime import datetime
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from backend.app.extensions import db
from backend.app.models.medical_record import MedicalRecord
from backend.app.models.appointment import Appointment
from backend.app.models.doctor import Doctor
from backend.app.utils.decorators import role_required
from backend.app.utils.errors import api_response, api_error

records_bp = Blueprint('records', __name__, url_prefix='/api/records')

@records_bp.route('', methods=['POST'])
@role_required(['doctor', 'admin'])
def create_medical_record():
    user_id = int(get_jwt_identity())
    claims = get_jwt()
    role = claims.get('role', 'doctor')
    data = request.get_json() or {}

    appointment_id = data.get('appointment_id')
    diagnosis_demo = data.get('diagnosis_demo', '').strip()
    notes = data.get('notes', '').strip()
    follow_up_str = data.get('follow_up_date')

    if not appointment_id:
        return api_error("appointment_id is required", code="VALIDATION_ERROR", status_code=400)

    appointment = db.session.get(Appointment, appointment_id)
    if not appointment:
        return api_error("Appointment not found", code="APPOINTMENT_NOT_FOUND", status_code=404)

    # Check if record already exists
    if appointment.medical_record:
        # Update existing record
        record = appointment.medical_record
        record.diagnosis_demo = diagnosis_demo
        record.notes = notes
    else:
        record = MedicalRecord(
            patient_id=appointment.patient_id,
            doctor_id=appointment.doctor_id,
            appointment_id=appointment.id,
            diagnosis_demo=diagnosis_demo,
            notes=notes
        )
        db.session.add(record)

    if follow_up_str:
        try:
            record.follow_up_date = datetime.strptime(follow_up_str, '%Y-%m-%d').date()
        except ValueError:
            pass

    # Mark appointment as completed
    appointment.status = 'COMPLETED'
    if appointment.queue_record:
        appointment.queue_record.queue_status = 'COMPLETED'
        appointment.queue_record.estimated_wait_minutes = 0

    db.session.commit()
    return api_response(record.to_dict(), message="Medical record saved successfully", status_code=201)

@records_bp.route('/patient/<int:patient_id>', methods=['GET'])
@jwt_required()
def get_patient_records(patient_id):
    records = MedicalRecord.query.filter_by(patient_id=patient_id).order_by(MedicalRecord.visit_date.desc()).all()
    return api_response([r.to_dict() for r in records])

@records_bp.route('/<int:rec_id>', methods=['GET'])
@jwt_required()
def get_record_by_id(rec_id):
    record = db.session.get(MedicalRecord, rec_id)
    if not record:
        return api_error("Record not found", code="RECORD_NOT_FOUND", status_code=404)
    return api_response(record.to_dict())
