import os
from flask import Flask, render_template, send_from_directory
from backend.app.config import config_by_name
from backend.app.extensions import db, jwt, cors
from backend.app.utils.errors import api_response, api_error

def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')

    base_dir = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    templates_dir = os.path.join(base_dir, 'templates')
    static_dir = os.path.join(base_dir, 'static')

    app = Flask(
        __name__,
        template_folder=templates_dir,
        static_folder=static_dir
    )
    
    app.config.from_object(config_by_name.get(config_name, config_by_name['default']))

    # Initialize Extensions
    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": app.config['CORS_ORIGINS']}})

    # JWT Error Handlers
    @jwt.unauthorized_loader
    def custom_unauthorized_response(err_msg):
        return api_error(f"Missing authorization header: {err_msg}", code="UNAUTHORIZED", status_code=401)

    @jwt.invalid_token_loader
    def custom_invalid_token_response(err_msg):
        return api_error(f"Invalid token: {err_msg}", code="INVALID_TOKEN", status_code=401)

    @jwt.expired_token_loader
    def custom_expired_token_response(jwt_header, jwt_payload):
        return api_error("The authentication token has expired. Please login again.", code="TOKEN_EXPIRED", status_code=401)

    # API Health Endpoint
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return api_response({
            'status': 'healthy',
            'version': '1.0.0',
            'database': 'connected'
        }, message="MediCare API is running")

    # Register Blueprints
    from backend.app.routes.auth import auth_bp
    from backend.app.routes.patients import patients_bp
    from backend.app.routes.doctors import doctors_bp
    from backend.app.routes.departments import dept_bp
    from backend.app.routes.appointments import appointments_bp
    from backend.app.routes.queue import queue_bp
    from backend.app.routes.records import records_bp
    from backend.app.routes.analytics import analytics_bp
    from backend.app.routes.predictions import predictions_bp
    from backend.app.routes.users import users_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(patients_bp)
    app.register_blueprint(doctors_bp)
    app.register_blueprint(dept_bp)
    app.register_blueprint(appointments_bp)
    app.register_blueprint(queue_bp)
    app.register_blueprint(records_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(predictions_bp)
    app.register_blueprint(users_bp)

    # Frontend Page Routes
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/login')
    def login_page():
        return render_template('login.html')

    @app.route('/register')
    def register_page():
        return render_template('register.html')

    # Patient views
    @app.route('/patient/dashboard')
    def patient_dashboard():
        return render_template('patient/dashboard.html')

    @app.route('/patient/book-appointment')
    def patient_book():
        return render_template('patient/book-appointment.html')

    @app.route('/patient/appointments')
    def patient_appointments():
        return render_template('patient/appointments.html')

    @app.route('/patient/queue')
    def patient_queue():
        return render_template('patient/queue.html')

    @app.route('/patient/records')
    def patient_records():
        return render_template('patient/records.html')

    # Doctor views
    @app.route('/doctor/dashboard')
    def doctor_dashboard():
        return render_template('doctor/dashboard.html')

    @app.route('/doctor/appointments')
    def doctor_appointments():
        return render_template('doctor/appointments.html')

    @app.route('/doctor/queue')
    def doctor_queue():
        return render_template('doctor/queue.html')

    # Admin views
    @app.route('/admin/dashboard')
    def admin_dashboard():
        return render_template('admin/dashboard.html')

    @app.route('/admin/analytics')
    def admin_analytics():
        return render_template('admin/analytics.html')

    @app.route('/admin/doctors')
    def admin_doctors():
        return render_template('admin/doctors.html')

    @app.route('/admin/departments')
    def admin_departments():
        return render_template('admin/departments.html')

    @app.route('/admin/users')
    def admin_users():
        return render_template('admin/users.html')

    # Global Error Handlers
    @app.errorhandler(404)
    def not_found_handler(e):
        return api_error("The requested URL was not found on the server", code="NOT_FOUND", status_code=404)

    @app.errorhandler(500)
    def internal_error_handler(e):
        return api_error("An internal server error occurred", code="INTERNAL_SERVER_ERROR", status_code=500)

    # Ensure tables are created
    with app.app_context():
        import backend.app.models
        db.create_all()

    return app
