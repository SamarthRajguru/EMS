from flask import Blueprint, request, jsonify
import jwt
from auth import token_required, role_required
from create_app import app, db
from models import Employee, Leave_managment
import sqlalchemy.exc

leave_bp = Blueprint("leave_bp", __name__)


@leave_bp.route("/accept", methods=["PUT"])
@token_required
@role_required("1")
def accept_leave():
    pass
    id = request.args.get("leave_id")
    application = (
        db.session.query(Leave_managment).filter(Leave_managment.leave_id == id).first()
    )
    print("applicarion: ", application)

    if application:
        application.leave_status = "Approved"
        db.session.commit()
        return jsonify({"msg": "Leave Application Approved"}), 200
    else:
        return jsonify({"msg": "Leave Application not exist"}), 404


@leave_bp.route("/decline", methods=["PUT"])
@token_required
@role_required("1")
def decline_leave():
    id = request.args.get("leave_id")
    application = (
        db.session.query(Leave_managment).filter(Leave_managment.leave_id == id).first()
    )
    print("application: ", application)

    if application:
        application.leave_status = "Declined"
        db.session.commit()
        return jsonify({"msg": "Leave Application Declined"}), 200
    else:
        return jsonify({"msg": "Leave Application not exist"}), 404


@leave_bp.route("/delete", methods=["PUT"])
@token_required
@role_required("1")
def delete_leave():

    id = request.args.get("leave_id")
    application = (
        db.session.query(Leave_managment).filter(Leave_managment.leave_id == id).first()
    )
    print("applicarion: ", application)

    if application:
        db.session.delete(application)
        db.session.commit()
        return jsonify({"msg": "Leave Application Deleted"}), 200
    else:
        return jsonify({"msg": "Application not exist"}), 404


