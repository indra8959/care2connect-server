from flask import Blueprint, request, jsonify
from auth.decorators import token_required
from models.appointment_model import create_appointment, get_appointment_by_id, get_all_appointments,update_appointment

appointment_bp = Blueprint("appointments", __name__, url_prefix="/appointments")

@appointment_bp.route("/create", methods=["POST"])
@token_required
def create(current_user):
    try:
        data = request.get_json()
        appointment_id = create_appointment(current_user,data)
        return jsonify({"message": "Appointment created", "appointment_id": appointment_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@appointment_bp.route("/<appointment_id>", methods=["GET"])
@token_required
def get_by_id(current_user, appointment_id):
    appt = get_appointment_by_id(appointment_id)
    if appt:
        return jsonify(appt)
    return jsonify({"error": "Appointment not found"}), 404

@appointment_bp.route("/<appointment_id>", methods=["POST"])
@token_required
def update(current_user, appointment_id):
    try:
        updated_data = request.get_json()
        success = update_appointment(appointment_id, updated_data)
        if success:
            return jsonify({"message": "Appointment updated successfully"})
        else:
            return jsonify({"error": "Appointment not found or no changes made"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@appointment_bp.route("get", methods=["GET"])
@token_required
def list_appointments(current_user):
    return jsonify(get_all_appointments(current_user))
