from backend.app.models.user import User
from backend.app.models.patient import Patient
from backend.app.models.doctor import Doctor
from backend.app.models.department import Department
from backend.app.models.schedule import DoctorSchedule
from backend.app.models.appointment import Appointment
from backend.app.models.queue import QueueRecord
from backend.app.models.medical_record import MedicalRecord
from backend.app.models.prediction import PredictionLog

__all__ = [
    'User',
    'Patient',
    'Doctor',
    'Department',
    'DoctorSchedule',
    'Appointment',
    'QueueRecord',
    'MedicalRecord',
    'PredictionLog'
]
