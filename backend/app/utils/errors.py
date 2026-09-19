from flask import jsonify

def api_response(data=None, message=None, status_code=200):
    response = {"success": True}
    if data is not None:
        response["data"] = data
    if message is not None:
        response["message"] = message
    return jsonify(response), status_code

def api_error(message, code="BAD_REQUEST", status_code=400, details=None):
    error_obj = {
        "code": code,
        "message": message
    }
    if details:
        error_obj["details"] = details
    return jsonify({
        "success": False,
        "error": error_obj
    }), status_code
