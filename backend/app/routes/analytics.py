from datetime import datetime, timedelta
from flask import Blueprint, request
from sqlalchemy import func
from backend.app.extensions import db
from backend.app.models.appointment import Appointment
from backend.app.models.doctor import Doctor
from backend.app.models.department import Department
from backend.app.models.queue import QueueRecord
from backend.app.utils.decorators import role_required
from backend.app.utils.errors import api_response

analytics_bp = Blueprint('analytics', __name__, url_prefix='/api/analytics')

@analytics_bp.route('/overview', methods=['GET'])
def get_overview():
    total_appointments = Appointment.query.count()
    completed_appointments = Appointment.query.filter_by(status='COMPLETED').count()
    cancelled_appointments = Appointment.query.filter_by(status='CANCELLED').count()
    no_show_appointments = Appointment.query.filter_by(status='NO_SHOW').count()
    active_in_queue = QueueRecord.query.filter_by(queue_status='WAITING').count()
    
    # Calculate average estimated wait time for waiting patients
    avg_wait = db.session.query(func.avg(QueueRecord.estimated_wait_minutes)).filter_by(queue_status='WAITING').scalar() or 0.0

    total_doctors = Doctor.query.filter_by(is_available=True).count()
    total_departments = Department.query.count()

    return api_response({
        'total_appointments': total_appointments,
        'completed_appointments': completed_appointments,
        'cancelled_appointments': cancelled_appointments,
        'no_show_appointments': no_show_appointments,
        'active_in_queue': active_in_queue,
        'average_wait_minutes': round(float(avg_wait), 1),
        'total_doctors': total_doctors,
        'total_departments': total_departments
    })

@analytics_bp.route('/appointments', methods=['GET'])
def get_appointment_trends():
    days = request.args.get('days', default=7, type=int)
    start_date = datetime.now().date() - timedelta(days=days)

    results = (
        db.session.query(
            Appointment.appointment_date,
            func.count(Appointment.id).label('total'),
            func.sum(db.case((Appointment.status == 'COMPLETED', 1), else_=0)).label('completed'),
            func.sum(db.case((Appointment.status == 'CANCELLED', 1), else_=0)).label('cancelled')
        )
        .filter(Appointment.appointment_date >= start_date)
        .group_by(Appointment.appointment_date)
        .order_by(Appointment.appointment_date.asc())
        .all()
    )

    data = [{
        'date': r.appointment_date.isoformat(),
        'total': int(r.total or 0),
        'completed': int(r.completed or 0),
        'cancelled': int(r.cancelled or 0)
    } for r in results]

    return api_response(data)

@analytics_bp.route('/departments', methods=['GET'])
def get_department_distribution():
    results = (
        db.session.query(
            Department.name,
            func.count(Appointment.id).label('appointment_count')
        )
        .outerjoin(Doctor, Doctor.department_id == Department.id)
        .outerjoin(Appointment, Appointment.doctor_id == Doctor.id)
        .group_by(Department.id, Department.name)
        .all()
    )

    data = [{
        'department': r.name,
        'count': int(r.appointment_count or 0)
    } for r in results]

    return api_response(data)

@analytics_bp.route('/waiting-times', methods=['GET'])
def get_waiting_time_trends():
    results = (
        db.session.query(
            Doctor.id,
            Doctor.specialization,
            func.avg(QueueRecord.estimated_wait_minutes).label('avg_wait')
        )
        .join(QueueRecord, QueueRecord.doctor_id == Doctor.id)
        .group_by(Doctor.id, Doctor.specialization)
        .all()
    )

    data = [{
        'doctor_id': r.id,
        'specialization': r.specialization,
        'avg_wait_minutes': round(float(r.avg_wait or 0), 1)
    } for r in results]

    return api_response(data)
