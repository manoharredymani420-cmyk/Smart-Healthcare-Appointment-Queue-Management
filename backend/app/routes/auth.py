from flask import Blueprint, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from backend.app.extensions import db
from backend.app.models.user import User
from backend.app.models.patient import Patient
from backend.app.models.doctor import Doctor
from backend.app.utils.security import hash_password, verify_password
from backend.app.utils.errors import api_response, api_error

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    name = data.get('name', '').strip()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    role = data.get('role', 'patient').strip().lower()

    if not name or not email or not password:
        return api_error("Name, email, and password are required", code="VALIDATION_ERROR", status_code=400)

    if role not in ['patient', 'doctor', 'admin']:
        return api_error("Invalid role specified", code="INVALID_ROLE", status_code=400)

    if User.query.filter_by(email=email).first():
        return api_error("User with this email already exists", code="EMAIL_ALREADY_EXISTS", status_code=409)

    # Create user
    user = User(
        name=name,
        email=email,
        password_hash=hash_password(password),
        role=role
    )
    db.session.add(user)
    db.session.flush()

    # Create role specific profile
    if role == 'patient':
        patient = Patient(
            user_id=user.id,
            phone=data.get('phone', ''),
            gender=data.get('gender', ''),
            address=data.get('address', '')
        )
        db.session.add(patient)
    elif role == 'doctor':
        doctor = Doctor(
            user_id=user.id,
            department_id=data.get('department_id'),
            specialization=data.get('specialization', 'General Practitioner'),
            experience_years=data.get('experience_years', 1),
            consultation_duration_minutes=data.get('consultation_duration_minutes', 15)
        )
        db.session.add(doctor)

    db.session.commit()

    # Generate token
    token = create_access_token(
        identity=str(user.id),
        additional_claims={'role': user.role, 'name': user.name, 'email': user.email}
    )

    return api_response({
        'user': user.to_dict(),
        'access_token': token
    }, message="Registration successful", status_code=201)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')

    if not email or not password:
        return api_error("Email and password are required", code="VALIDATION_ERROR", status_code=400)

    user = User.query.filter_by(email=email).first()
    if not user or not verify_password(password, user.password_hash):
        return api_error("Invalid email or password", code="INVALID_CREDENTIALS", status_code=401)

    if not user.is_active:
        return api_error("This account has been deactivated", code="ACCOUNT_INACTIVE", status_code=403)

    token = create_access_token(
        identity=str(user.id),
        additional_claims={'role': user.role, 'name': user.name, 'email': user.email}
    )

    extra_data = {}
    if user.role == 'patient' and user.patient:
        extra_data['patient_id'] = user.patient.id
    elif user.role == 'doctor' and user.doctor:
        extra_data['doctor_id'] = user.doctor.id

    return api_response({
        'user': {**user.to_dict(), **extra_data},
        'access_token': token
    }, message="Login successful")

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    user_id = int(get_jwt_identity())
    user = db.session.get(User, user_id)
    if not user:
        return api_error("User not found", code="USER_NOT_FOUND", status_code=404)

    user_info = user.to_dict()
    if user.role == 'patient' and user.patient:
        user_info['patient_profile'] = user.patient.to_dict()
    elif user.role == 'doctor' and user.doctor:
        user_info['doctor_profile'] = user.doctor.to_dict()

    return api_response(user_info)
