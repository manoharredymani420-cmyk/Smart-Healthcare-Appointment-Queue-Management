from flask import Blueprint, request
from backend.app.extensions import db
from backend.app.models.user import User
from backend.app.utils.decorators import role_required
from backend.app.utils.errors import api_response, api_error

users_bp = Blueprint('users', __name__, url_prefix='/api/users')

@users_bp.route('', methods=['GET'])
@role_required(['admin'])
def list_users():
    role = request.args.get('role')
    query = User.query
    if role:
        query = query.filter_by(role=role.lower())
    users = query.order_by(User.id.asc()).all()
    return api_response([u.to_dict() for u in users])

@users_bp.route('/<int:user_id>/toggle-status', methods=['PUT'])
@role_required(['admin'])
def toggle_user_status(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return api_error("User not found", code="USER_NOT_FOUND", status_code=404)

    user.is_active = not user.is_active
    db.session.commit()
    return api_response(user.to_dict(), message=f"User {'activated' if user.is_active else 'deactivated'} successfully")
