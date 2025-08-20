from flask import Blueprint, request, jsonify
from datetime import datetime
from models.slot_model import insert_or_update_slot, get_all_disabled_slots,dateandtime
from auth.decorators import token_required
slot_bp = Blueprint("slot_bp", __name__)

@slot_bp.route("/slot_disable", methods=["POST"])
@token_required
def slot_disable(current_user):
    try:
        data = request.json
        input_str = data.get("date") + data.get("slot")

        date_part = input_str[:10]
        time_part = input_str[10:19].strip()
        dt = datetime.strptime(date_part + time_part, "%Y-%m-%d%I:%M %p")
        formatted = dt.strftime("%Y%m%d%H")

        mdata = {
            "_id": formatted,
            "date": data.get("date"),
            "slot": data.get("slot"),
            "enable": data.get("enable"),
            "doctor_id": data.get("doctor_id") or "67ee5e1bde4cb48c515073ee"
        }

        inserted_id = insert_or_update_slot(mdata)
        return jsonify({"inserted_id": inserted_id}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@slot_bp.route("/get_slot", methods=["GET"])
@token_required
def get_slot(current_user):
    try:
        documents = get_all_disabled_slots()
        if not documents:
            return jsonify({"error": "No disabled slots found"}), 404

        return jsonify(documents), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@slot_bp.route("/get_date_schedule/<doctor_id>", methods=["GET","OPTIONS"])
# @token_required
def get_date_schedule(doctor_id):
    try:
        data = dateandtime('date',doctor_id)
        if not data:
            return jsonify({"error": "No disabled slots found"}), 404
        return jsonify(data), 200
    except Exception as e:
        print({"error": str(e)})
        return jsonify({"error": str(e)}), 500
    
@slot_bp.route("/get_time_schedule/<doctor_id>/<date>", methods=["GET","OPTIONS"])
# @token_required
def get_time_schedule(doctor_id,date):
    try:
        data = dateandtime(date,doctor_id)
        if not data:
            return jsonify({"error": "No time slots found"}), 404
        return jsonify(data), 200
    except Exception as e:
        print({"error": str(e)})
        return jsonify({"error": str(e)}), 500
