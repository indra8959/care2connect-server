# auth/decorators.py

import jwt
from flask import request, jsonify
from functools import wraps
from config import JWT_SECRET_KEY
from models.user_model import get_user_by_id

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.method == "OPTIONS":
            return '', 200  # Let preflight pass without token check
        token = None

        # Get token from header
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]

        if not token:
            return jsonify({'error': 'Token is missing'}), 401

        try:
            decoded = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
            user_id = decoded.get('user_id')
            current_user = get_user_by_id(user_id)

            if not current_user:
                return jsonify({'error': 'User not found'}), 401

        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401

        # Inject current_user into the route
        return f(current_user, *args, **kwargs)

    return decorated
