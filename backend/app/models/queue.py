from datetime import datetime, timezone
from backend.app.extensions import db

class QueueRecord(db.Model):
    __tablename__ = 'queue_records'

    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id', ondelete='CASCADE'), unique=True, nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id', ondelete='CASCADE'), nullable=False, index=True)
    queue_position = db.Column(db.Integer, nullable=False, default=1)
    patients_ahead = db.Column(db.Integer, nullable=False, default=0)
    estimated_wait_minutes = db.Column(db.Integer, nullable=False, default=0)
    queue_status = db.Column(db.String(20), nullable=False, default='WAITING')  # WAITING, CALLED, IN_PROGRESS, COMPLETED, SKIPPED
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'id': self.id,
            'appointment_id': self.appointment_id,
            'doctor_id': self.doctor_id,
            'doctor_name': self.appointment.doctor.user.name if self.appointment and self.appointment.doctor and self.appointment.doctor.user else None,
            'patient_name': self.appointment.patient.user.name if self.appointment and self.appointment.patient and self.appointment.patient.user else None,
            'token_number': self.appointment.token_number if self.appointment else None,
            'appointment_date': self.appointment.appointment_date.isoformat() if self.appointment and self.appointment.appointment_date else None,
            'appointment_time': self.appointment.appointment_time.strftime('%H:%M') if self.appointment and self.appointment.appointment_time else None,
            'queue_position': self.queue_position,
            'patients_ahead': self.patients_ahead,
            'estimated_wait_minutes': self.estimated_wait_minutes,
            'queue_status': self.queue_status,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
