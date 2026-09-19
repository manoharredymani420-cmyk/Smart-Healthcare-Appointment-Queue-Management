from datetime import datetime
from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from backend.app.extensions import db
from backend.app.models.queue import QueueRecord
from backend.app.models.appointment import Appointment
from backend.app.services.queue_service import call_next_patient, recalculate_doctor_queue
from backend.app.utils.decorators import role_required
from backend.app.utils.errors import api_response, api_error

queue_bp = Blueprint('queue', __name__, url_prefix='/api/queue')

@queue_bp.route('/<int:appointment_id>', methods=['GET'])
def get_appointment_queue(appointment_id):
    queue_rec = QueueRecord.query.filter_by(appointment_id=appointment_id).first()
    if not queue_rec:
        return api_error("Queue record not found", code="QUEUE_NOT_FOUND", status_code=404)
    return api_response(queue_rec.to_dict())

@queue_bp.route('/doctor/<int:doctor_id>/next', methods=['POST'])
@role_required(['doctor', 'admin'])
def next_in_queue(doctor_id):
    date_str = request.args.get('date')
    if date_str:
        try:
            target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            target_date = datetime.now().date()
    else:
        target_date = datetime.now().date()

    next_appt = call_next_patient(doctor_id, target_date)
    if not next_appt:
        return api_response(None, message="No more waiting patients in queue for today")

    return api_response(next_appt.to_dict(), message=f"Called next patient: Token {next_appt.token_number}")

@queue_bp.route('/<int:appointment_id>/status', methods=['PUT'])
@role_required(['doctor', 'admin'])
def update_queue_status(appointment_id):
    queue_rec = QueueRecord.query.filter_by(appointment_id=appointment_id).first()
    if not queue_rec:
        return api_error("Queue record not found", code="QUEUE_NOT_FOUND", status_code=404)

    data = request.get_json() or {}
    status = data.get('status', '').upper()
    valid_statuses = ['WAITING', 'CALLED', 'IN_PROGRESS', 'COMPLETED', 'SKIPPED']

    if status not in valid_statuses:
        return api_error(f"Invalid queue status. Must be one of: {', '.join(valid_statuses)}", 
                         code="INVALID_STATUS", status_code=400)

    queue_rec.queue_status = status
    if queue_rec.appointment:
        if status == 'COMPLETED':
            queue_rec.appointment.status = 'COMPLETED'
            queue_rec.estimated_wait_minutes = 0
        elif status == 'SKIPPED':
            queue_rec.appointment.status = 'NO_SHOW'
            queue_rec.estimated_wait_minutes = 0
        elif status in ['CALLED', 'IN_PROGRESS']:
            queue_rec.appointment.status = 'IN_PROGRESS'
            queue_rec.estimated_wait_minutes = 0

    db.session.commit()
    recalculate_doctor_queue(queue_rec.doctor_id, queue_rec.appointment.appointment_date)
    return api_response(queue_rec.to_dict(), message="Queue status updated successfully")
