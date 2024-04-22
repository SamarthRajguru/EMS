from flask import Blueprint, jsonify, request
from auth import token_required, role_required

home_bp = Blueprint("home_bp", __name__)


@home_bp.route("/", methods=["GET"])
@token_required
@role_required("2")
def index():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    return "Welcome!"
