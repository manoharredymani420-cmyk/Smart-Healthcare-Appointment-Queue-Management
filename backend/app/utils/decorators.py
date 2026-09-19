from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from backend.app.utils.errors import api_error

def role_required(allowed_roles):
    """
    Decorator to restrict route access to specific roles.
    allowed_roles: list of allowed roles e.g. ['admin', 'doctor', 'patient'] or string
    """
    if isinstance(allowed_roles, str):
        allowed_roles = [allowed_roles]
        
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            user_role = claims.get('role', '')
            if user_role not in allowed_roles:
                return api_error("Forbidden: You do not have permission to access this resource", 
                                 code="FORBIDDEN", status_code=403)
            return fn(*args, **kwargs)
        return wrapper
    return decorator
