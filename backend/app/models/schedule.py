from backend.app.extensions import db

class DoctorSchedule(db.Model):
    __tablename__ = 'doctor_schedules'

    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id', ondelete='CASCADE'), nullable=False, index=True)
    day_of_week = db.Column(db.Integer, nullable=False)  # 0=Monday, 1=Tuesday, ... 6=Sunday
    start_time = db.Column(db.Time, nullable=False)      # e.g., 09:00:00
    end_time = db.Column(db.Time, nullable=False)        # e.g., 17:00:00
    slot_duration_minutes = db.Column(db.Integer, default=15, nullable=False)
    max_appointments = db.Column(db.Integer, default=20, nullable=False)

    DAY_NAMES = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    def to_dict(self):
        return {
            'id': self.id,
            'doctor_id': self.doctor_id,
            'day_of_week': self.day_of_week,
            'day_name': self.DAY_NAMES[self.day_of_week] if 0 <= self.day_of_week <= 6 else 'Unknown',
            'start_time': self.start_time.strftime('%H:%M') if self.start_time else None,
            'end_time': self.end_time.strftime('%H:%M') if self.end_time else None,
            'slot_duration_minutes': self.slot_duration_minutes,
            'max_appointments': self.max_appointments
        }
