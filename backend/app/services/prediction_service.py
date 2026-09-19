import os
import joblib
import pandas as pd
from flask import current_app

_model_cache = None

def get_ml_model():
    global _model_cache
    if _model_cache is not None:
        return _model_cache

    model_path = current_app.config.get('ML_MODEL_PATH')
    if model_path and os.path.exists(model_path):
        try:
            _model_cache = joblib.load(model_path)
            return _model_cache
        except Exception as e:
            current_app.logger.error(f"Error loading ML model: {e}")
    return None

def predict_wait_time(
    doctor_id: int,
    department_id: int = 1,
    day_of_week: int = 0,
    appointment_hour: int = 10,
    patients_ahead: int = 0,
    queue_length: int = 0,
    average_consultation_time: float = 15.0,
    appointments_scheduled: int = 10,
    historical_average_wait: float = None
) -> dict:
    """
    Predicts waiting time in minutes using the trained ML model.
    Falls back to deterministic calculation if the model is unavailable.
    """
    if patients_ahead <= 0:
        return {
            'estimated_wait_minutes': 0,
            'model_version': 'deterministic',
            'method': 'direct_zero'
        }

    if historical_average_wait is None:
        historical_average_wait = patients_ahead * average_consultation_time * 0.9

    artifact = get_ml_model()
    if artifact and 'model' in artifact:
        try:
            features = pd.DataFrame([{
                'doctor_id': doctor_id,
                'department_id': department_id,
                'day_of_week': day_of_week,
                'appointment_hour': appointment_hour,
                'patients_ahead': patients_ahead,
                'queue_length': max(queue_length, patients_ahead + 1),
                'average_consultation_time': average_consultation_time,
                'appointments_scheduled': appointments_scheduled,
                'historical_average_wait': historical_average_wait
            }])
            pred = artifact['model'].predict(features)[0]
            estimated = max(0, round(float(pred), 1))
            return {
                'estimated_wait_minutes': estimated,
                'model_version': artifact.get('version', 'v1.0'),
                'model_name': artifact.get('model_name', 'Gradient Boosting'),
                'method': 'ml_prediction'
            }
        except Exception as e:
            if current_app:
                current_app.logger.warning(f"ML prediction failed, falling back to baseline: {e}")

    # Baseline formula: patients_ahead * average_consultation_time
    baseline_wait = max(0, round(patients_ahead * average_consultation_time, 1))
    return {
        'estimated_wait_minutes': baseline_wait,
        'model_version': 'baseline-v1',
        'model_name': 'Deterministic Rule',
        'method': 'baseline'
    }
