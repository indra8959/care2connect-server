from flask import Blueprint, request, jsonify
from models.hospital_model import create_hospital, get_hospital_by_id, list_hospitals
from auth.decorators import token_required
hospital_bp = Blueprint('hospital_bp', __name__,url_prefix='/hospitals')

@hospital_bp.route('/create', methods=['POST'])
@token_required
def add_hospital(current_user):
    data = request.get_json()
    hospital_id = create_hospital(data)
    return jsonify({"message": "Hospital created", "hospital_id": hospital_id}), 201

@hospital_bp.route('/<hospital_id>', methods=['GET'])
# @token_required
def fetch_hospital(hospital_id):
    hospital = get_hospital_by_id(hospital_id)
    if not hospital:
        return jsonify({"error": "Hospital not found"}), 404
    return jsonify(hospital), 200

@hospital_bp.route('/get', methods=['GET'])
# @token_required
def fetch_hospitals():
    hospitals = list_hospitals()
    return jsonify(hospitals), 200
