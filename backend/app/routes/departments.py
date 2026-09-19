from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from backend.app.extensions import db
from backend.app.models.department import Department
from backend.app.utils.decorators import role_required
from backend.app.utils.errors import api_response, api_error

dept_bp = Blueprint('departments', __name__, url_prefix='/api/departments')

@dept_bp.route('', methods=['GET'])
def list_departments():
    departments = Department.query.order_by(Department.name.asc()).all()
    return api_response([d.to_dict() for d in departments])

@dept_bp.route('/<int:dept_id>', methods=['GET'])
def get_department(dept_id):
    dept = db.session.get(Department, dept_id)
    if not dept:
        return api_error("Department not found", code="DEPARTMENT_NOT_FOUND", status_code=404)
    return api_response(dept.to_dict())

@dept_bp.route('', methods=['POST'])
@role_required(['admin'])
def create_department():
    data = request.get_json() or {}
    name = data.get('name', '').strip()
    description = data.get('description', '').strip()

    if not name:
        return api_error("Department name is required", code="VALIDATION_ERROR", status_code=400)

    if Department.query.filter_by(name=name).first():
        return api_error("Department with this name already exists", code="DUPLICATE_NAME", status_code=409)

    dept = Department(name=name, description=description)
    db.session.add(dept)
    db.session.commit()

    return api_response(dept.to_dict(), message="Department created successfully", status_code=201)

@dept_bp.route('/<int:dept_id>', methods=['PUT'])
@role_required(['admin'])
def update_department(dept_id):
    dept = db.session.get(Department, dept_id)
    if not dept:
        return api_error("Department not found", code="DEPARTMENT_NOT_FOUND", status_code=404)

    data = request.get_json() or {}
    if 'name' in data and data['name'].strip():
        dept.name = data['name'].strip()
    if 'description' in data:
        dept.description = data['description'].strip()

    db.session.commit()
    return api_response(dept.to_dict(), message="Department updated successfully")

@dept_bp.route('/<int:dept_id>', methods=['DELETE'])
@role_required(['admin'])
def delete_department(dept_id):
    dept = db.session.get(Department, dept_id)
    if not dept:
        return api_error("Department not found", code="DEPARTMENT_NOT_FOUND", status_code=404)

    if dept.doctors.count() > 0:
        return api_error("Cannot delete department with assigned doctors", code="DEPENDENCY_EXISTS", status_code=400)

    db.session.delete(dept)
    db.session.commit()
    return api_response(message="Department deleted successfully")
