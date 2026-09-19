from datetime import datetime, timezone
from backend.app.extensions import db

class Doctor(db.Model):
    __tablename__ = 'doctors'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), unique=True, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id', ondelete='SET NULL'), nullable=True)
    specialization = db.Column(db.String(100), nullable=False)
    experience_years = db.Column(db.Integer, default=0)
    consultation_duration_minutes = db.Column(db.Integer, default=15)
    is_available = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    schedules = db.relationship('DoctorSchedule', backref='doctor', cascade='all, delete-orphan', lazy='dynamic')
    appointments = db.relationship('Appointment', backref='doctor', lazy='dynamic')
    medical_records = db.relationship('MedicalRecord', backref='doctor', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.user.name if self.user else None,
            'email': self.user.email if self.user else None,
            'department_id': self.department_id,
            'department_name': self.department.name if self.department else None,
            'specialization': self.specialization,
            'experience_years': self.experience_years,
            'consultation_duration_minutes': self.consultation_duration_minutes,
            'is_available': self.is_available,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
