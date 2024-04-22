# this file is for role required and token required decoreator and token generation

from create_app import app
from flask import request, jsonify
from functools import wraps
import jwt
from datetime import datetime, timedelta


def generate_JWT_token(email, role_id):
    expiration_time = datetime.now() + timedelta(minutes=1)
    payload = {"email": email, "role_id": role_id, "exp": expiration_time}
    token = jwt.encode(payload, app.config["SECRET_KEY"], algorithm="HS256")
    return token


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"error": "Token is missing"}), 403
        try:
            token = token.split(" ")[1]
            # payload = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            return f(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 403
        except jwt.InvalidTokenError:
            return jsonify({"error": "Token is invalid"}), 403

    return decorated


def role_required(role_id):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            token = request.headers.get("Authorization")
            if token:
                try:
                    token = token.split(" ")[1]
                    payload = jwt.decode(
                        token, app.config["SECRET_KEY"], algorithms=["HS256"]
                    )
                    user_role = str(payload.get("role_id"))
                    print("user_rolee", type(user_role), user_role)
                    print("as", user_role)
                    print("role_id", type(role_id), role_id)
                    if user_role == role_id:
                        return func(*args, **kwargs)
                    else:
                        return jsonify({"error": "insufficient permission"}), 403
                except jwt.ExpiredSignatureError:
                    return jsonify({"error": "Token has expired"}), 401
                except jwt.InvalidTokenError:
                    return jsonify({"error": "Token is invalid"}), 401
            else:
                return jsonify({"error": "Token is missing"}), 401

        return wrapper

    return decorator
