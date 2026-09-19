from datetime import datetime, timezone
from backend.app.extensions import db

class PredictionLog(db.Model):
    __tablename__ = 'prediction_logs'

    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id', ondelete='CASCADE'), nullable=False, index=True)
    model_version = db.Column(db.String(50), nullable=False, default='v1.0')
    predicted_wait_minutes = db.Column(db.Float, nullable=False)
    actual_wait_minutes = db.Column(db.Float, nullable=True)
    prediction_created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'id': self.id,
            'appointment_id': self.appointment_id,
            'model_version': self.model_version,
            'predicted_wait_minutes': round(self.predicted_wait_minutes, 1),
            'actual_wait_minutes': round(self.actual_wait_minutes, 1) if self.actual_wait_minutes is not None else None,
            'prediction_created_at': self.prediction_created_at.isoformat() if self.prediction_created_at else None
        }
