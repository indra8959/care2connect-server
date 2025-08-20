from flask import Blueprint, request, jsonify
from models.doctor_model import create_doctor, get_doctor_by_id, list_doctors,update_doctor,create_doctor_onboard,application_list,get_onboarding_by_id,update_doctor_application,get_doctor_by_user_id,get_onboarding_by_user_id
from auth.decorators import token_required 

doctor_bp = Blueprint('doctor_bp', __name__)

@doctor_bp.route('/doctors', methods=['POST'])
@token_required
def add_doctor(current_user):
    data = request.get_json()
    try:
        doctor_id = create_doctor(data)
        return jsonify({"message": "Doctor created", "doctor_id": doctor_id}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@doctor_bp.route('/doctors/<doctor_id>', methods=['GET'])
# @token_required
def fetch_doctor(doctor_id):
    doctor = get_doctor_by_id(doctor_id,"user")
    if not doctor:
        return jsonify({"error": "Doctor not found"}), 404
    return jsonify(doctor), 200

@doctor_bp.route('/admin/doctors/<doctor_id>', methods=['GET'])
@token_required
def fetch_doctor_admin(current_user,doctor_id):
    doctor = get_doctor_by_id(doctor_id,"admin")
    if not doctor:
        return jsonify({"error": "Doctor not found"}), 404
    return jsonify(doctor), 200


@doctor_bp.route("/doctors/<doctor_id>", methods=["POST"])
@token_required
def update(current_user, doctor_id):
    try:
        updated_data = request.get_json()
        success = update_doctor(doctor_id, updated_data)
        if success:
            return jsonify({"message": "Doctor updated successfully"}),200
        else:
            return jsonify({"error": "Doctor not found or no changes made"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@doctor_bp.route('/doctors', methods=['GET'])
def fetch_doctors():
    doctors = list_doctors()
    return jsonify(doctors), 200

@doctor_bp.route('/onboard', methods=['POST'])
# @token_required
def onboard_doctor():
    data = request.get_json()
    try:
        id = create_doctor_onboard(data)
        return jsonify({"message": "Doctor Onboarded", "id":id}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# @doctor_bp.route('/onboard', methods=['POST'])
# @token_required
# def onboard_doctor(current_user):
#     data = request.get_json()
#     try:
#         id = create_doctor_onboard(data,current_user)
#         return jsonify({"message": "Doctor Onboarded", "id":id}), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

@doctor_bp.route('/doctor/onboard/<onboard_id>', methods=['GET'])
@token_required
def fetch_onboard_application(current_user,onboard_id):
    app = get_onboarding_by_id(onboard_id)
    if not app:
        return jsonify({"error": "Applcation not found"}), 404
    return jsonify(app), 200

@doctor_bp.route("/doctor/onboard/<onboard_id>", methods=["POST"])
@token_required
def update_doctor_onboard(current_user, onboard_id):
    try:
        updated_data = request.get_json()
        success = update_doctor_application(onboard_id, updated_data)
        if success:
            return jsonify({"message": "Application updated successfully"}),200
        else:
            return jsonify({"error": "Application not found or no changes made"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@doctor_bp.route('/onboard_list', methods=['GET'])
@token_required
def onboard_doctor_list(current_user):
    applications = application_list()
    return jsonify(applications), 200

@doctor_bp.route('/find_doctor', methods=['GET'])
@token_required
def find_doctor(current_user):
    doctor = get_doctor_by_user_id(current_user['phone'])
    if not doctor:
        application = get_onboarding_by_user_id(current_user['phone'])
        if not application:
            return jsonify({"error": "Doctor not found"}), 404
        else:
            return jsonify({"status":application.get('status','pending')}), 200
    else:
        return jsonify(doctor['_id']), 200
