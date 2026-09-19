from datetime import datetime, timezone
from backend.app.extensions import db

class MedicalRecord(db.Model):
    __tablename__ = 'medical_records'

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id', ondelete='CASCADE'), nullable=False, index=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id', ondelete='CASCADE'), nullable=False, index=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id', ondelete='CASCADE'), unique=True, nullable=False)
    visit_date = db.Column(db.Date, nullable=False, default=lambda: datetime.now(timezone.utc).date())
    diagnosis_demo = db.Column(db.String(255), nullable=True)  # Demo label e.g., "Seasonal Flu", "Routine Checkup"
    notes = db.Column(db.Text, nullable=True)
    follow_up_date = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'patient_name': self.patient.user.name if self.patient and self.patient.user else None,
            'doctor_id': self.doctor_id,
            'doctor_name': self.doctor.user.name if self.doctor and self.doctor.user else None,
            'department_name': self.doctor.department.name if self.doctor and self.doctor.department else None,
            'appointment_id': self.appointment_id,
            'visit_date': self.visit_date.isoformat() if self.visit_date else None,
            'diagnosis_demo': self.diagnosis_demo,
            'notes': self.notes,
            'follow_up_date': self.follow_up_date.isoformat() if self.follow_up_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
