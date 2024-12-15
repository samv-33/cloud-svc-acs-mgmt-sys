from flask import Blueprint, request, jsonify
from services import create_user as create_user_service, get_user as get_user_service
from schemas import User

users_bp = Blueprint('users', __name__)

@users_bp.route('/users', methods=['POST'])
def create_user_endpoint():
    user_data = request.get_json()
    user = User(**user_data)
    user_id = create_user_service(user)
    return jsonify({"user_id": user_id}), 201

@users_bp.route('/users/<user_id>', methods=['GET'])
def get_user_endpoint(user_id):
    user = get_user_service(user_id)
    if user:
        return jsonify(user)
    else:
        return jsonify({"message": "User not found"}), 404