from flask import Blueprint, request, jsonify
import jwt
from auth import role_required, token_required
from models import Attendance, Employee
from create_app import app, db
import datetime


attendance_bp = Blueprint("attendance_bp", __name__)


@attendance_bp.route("/take")
@token_required
def create():

    halfday = bool(request.args.get("halfday"))
    print("halfday :", halfday, type(halfday))
    present = True
    date = datetime.datetime.today().date()

    # getting deatils from token
    token = request.headers.get("Authorization")
    token = token.split(" ")[1]
    payload = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
    print("rachead ", payload["email"])
    email = payload["email"]
    user = db.session.query(Employee).filter(Employee.email == email).first()
    print("1")
    emp_id = user.emp_id
    print("check_user : ", user)

    new_attendance = Attendance(
        emp_id=emp_id,
        present=present,
        on_halfday=halfday,
        date=date,
    )

    try:
        db.session.add(new_attendance)
        db.session.commit()
        return jsonify({"msg": "Attendance added"})
    except Exception as e:
        return jsonify({"err": str(e)})


# API to view employee's attendence
@attendance_bp.route("/get")
@token_required
def retrive():
    pass
    # getting deatils from token
    token = request.headers.get("Authorization")
    token = token.split(" ")[1]
    payload = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
    print(payload["email"])
    email = payload["email"]
    user = db.session.query(Employee).filter(Employee.email == email).first()
    emp_id = user.emp_id

    fullday = db.session.query(Attendance).filter(Attendance.emp_id == emp_id).count()
    halfdays = (
        db.session.query(Attendance)
        .filter(Attendance.emp_id == emp_id)
        .where(Attendance.on_halfday == True)
        .count()
    )

    print("fullday: ", fullday)
    print("Halfdays :", halfdays)
    return jsonify(
        {"emp_id": emp_id, "Total attendence": fullday, "Halfdays": halfdays}
    )
