from datetime import datetime, timezone
from backend.app.extensions import db

class Department(db.Model):
    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    doctors = db.relationship('Doctor', backref='department', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'doctor_count': self.doctors.count() if hasattr(self.doctors, 'count') else len(self.doctors),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
