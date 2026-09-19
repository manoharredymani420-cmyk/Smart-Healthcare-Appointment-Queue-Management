from flask import Blueprint, request
from backend.app.extensions import db
from backend.app.models.appointment import Appointment
from backend.app.models.prediction import PredictionLog
from backend.app.services.prediction_service import predict_wait_time
from backend.app.utils.errors import api_response, api_error

predictions_bp = Blueprint('predictions', __name__, url_prefix='/api/predictions')

@predictions_bp.route('/waiting-time', methods=['POST'])
def predict():
    data = request.get_json() or {}
    doctor_id = data.get('doctor_id')
    patients_ahead = data.get('patients_ahead')

    if doctor_id is None or patients_ahead is None:
        return api_error("doctor_id and patients_ahead are required", code="VALIDATION_ERROR", status_code=400)

    department_id = data.get('department_id', 1)
    day_of_week = data.get('day_of_week', 0)
    appointment_hour = data.get('appointment_hour', 10)
    queue_length = data.get('queue_length', max(patients_ahead + 1, 1))
    average_consultation_time = data.get('average_consultation_time', 15.0)

    prediction = predict_wait_time(
        doctor_id=int(doctor_id),
        department_id=int(department_id),
        day_of_week=int(day_of_week),
        appointment_hour=int(appointment_hour),
        patients_ahead=int(patients_ahead),
        queue_length=int(queue_length),
        average_consultation_time=float(average_consultation_time)
    )

    appointment_id = data.get('appointment_id')
    if appointment_id:
        log = PredictionLog(
            appointment_id=appointment_id,
            model_version=prediction.get('model_version', 'v1.0'),
            predicted_wait_minutes=prediction.get('estimated_wait_minutes', 0.0)
        )
        db.session.add(log)
        db.session.commit()

    return api_response(prediction)

@predictions_bp.route('/<int:appointment_id>', methods=['GET'])
def get_appointment_prediction(appointment_id):
    appointment = db.session.get(Appointment, appointment_id)
    if not appointment:
        return api_error("Appointment not found", code="APPOINTMENT_NOT_FOUND", status_code=404)

    # Check existing prediction log
    latest_log = (
        PredictionLog.query
        .filter_by(appointment_id=appointment_id)
        .order_by(PredictionLog.prediction_created_at.desc())
        .first()
    )

    if latest_log:
        return api_response(latest_log.to_dict())

    # Dynamically compute prediction
    patients_ahead = appointment.queue_record.patients_ahead if appointment.queue_record else 0
    pred = predict_wait_time(
        doctor_id=appointment.doctor_id,
        department_id=appointment.doctor.department_id if appointment.doctor else 1,
        day_of_week=appointment.appointment_date.weekday(),
        appointment_hour=appointment.appointment_time.hour,
        patients_ahead=patients_ahead,
        queue_length=patients_ahead + 1,
        average_consultation_time=float(appointment.doctor.consultation_duration_minutes if appointment.doctor else 15)
    )
    return api_response(pred)
