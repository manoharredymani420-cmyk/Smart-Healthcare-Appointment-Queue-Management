from datetime import datetime, timezone
from backend.app.extensions import db

class Appointment(db.Model):
    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id', ondelete='CASCADE'), nullable=False, index=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id', ondelete='CASCADE'), nullable=False, index=True)
    appointment_date = db.Column(db.Date, nullable=False, index=True)
    appointment_time = db.Column(db.Time, nullable=False)
    token_number = db.Column(db.String(20), nullable=False)  # e.g., T-01, D1-001
    status = db.Column(db.String(20), default='BOOKED', nullable=False, index=True)
    # Statuses: BOOKED, CONFIRMED, WAITING, IN_PROGRESS, COMPLETED, CANCELLED, NO_SHOW
    reason = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    queue_record = db.relationship('QueueRecord', backref='appointment', uselist=False, cascade='all, delete-orphan')
    medical_record = db.relationship('MedicalRecord', backref='appointment', uselist=False, cascade='all, delete-orphan')
    prediction_logs = db.relationship('PredictionLog', backref='appointment', cascade='all, delete-orphan', lazy='dynamic')

    __table_args__ = (
        db.UniqueConstraint('doctor_id', 'appointment_date', 'appointment_time', name='uq_doctor_datetime'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'patient_name': self.patient.user.name if self.patient and self.patient.user else None,
            'patient_phone': self.patient.phone if self.patient else None,
            'doctor_id': self.doctor_id,
            'doctor_name': self.doctor.user.name if self.doctor and self.doctor.user else None,
            'department_name': self.doctor.department.name if self.doctor and self.doctor.department else None,
            'appointment_date': self.appointment_date.isoformat() if self.appointment_date else None,
            'appointment_time': self.appointment_time.strftime('%H:%M') if self.appointment_time else None,
            'token_number': self.token_number,
            'status': self.status,
            'reason': self.reason,
            'queue_position': self.queue_record.queue_position if self.queue_record else None,
            'patients_ahead': self.queue_record.patients_ahead if self.queue_record else None,
            'estimated_wait_minutes': self.queue_record.estimated_wait_minutes if self.queue_record else None,
            'queue_status': self.queue_record.queue_status if self.queue_record else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
