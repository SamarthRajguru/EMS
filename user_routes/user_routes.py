from flask import Blueprint, request, jsonify
import jwt
import sqlalchemy
from auth import token_required
from create_app import app, db
from models import Employee, Policy, Leave_managment, Attendance

user_routes_bp = Blueprint("user_routes_bp", __name__)


# API to view Employee details
@user_routes_bp.route("/get", methods=["GET"])
@token_required
def retrive_one():
    data = request.args.get("emp_id")
    print(data)
    user = db.session.query(Employee).filter(Employee.emp_id == data).first()

    if user:
        print("This is User", user)
        users_list = [
            {
                "id": user.emp_id,
                "name": user.name,
                "email": user.email,
                "contact": user.contact,
                "role": user.role_id,
            }
        ]
        return jsonify(users_list)
    else:
        return jsonify({"Message": "User not found"})


# API to view policy
@user_routes_bp.route("/view_policy")
@token_required
def get_all_policy():
    page_no = request.args.get("page_no", default=1, type=int)
    per_page = request.args.get("per_page", default=5, type=int)
    if page_no < 1:
        return jsonify({"message": "Invalid Page number. Page number starts from 1"})

    else:
        offset = (page_no - 1) * per_page
        total_count = db.session.query(Policy).count()
        items = db.session.query(Policy).offset(offset).limit(per_page).all()

        policy_list = []

        for policy in items:
            policy_dict = {
                "id": policy.id,
                "description": policy.description,
                "date_created": policy.date_created,
            }
            policy_list.append(policy_dict)

        response = {
            "total_count": total_count,
            "page_no": page_no,
            "per_page": per_page,
            "pets": policy_list,
        }

        return jsonify(response)


# API to apply for leave
@user_routes_bp.route("/apply_leave", methods=["POST"])
@token_required
def apply_leave():
    data = request.get_json()
    reason = data.get("reason")
    from_date = data.get("from_date")
    to_date = data.get("to_date")
    status = "Pending"

    # getting deatils from token
    token = request.headers.get("Authorization")
    token = token.split(" ")[1]
    payload = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
    print(payload["email"])
    email = payload["email"]

    user = db.session.query(Employee).filter(Employee.email == email).first()
    emp_id = user.emp_id
    print("check_user : ", user)
    print("got Id successfully ", emp_id)
    if user:
        new_leave = Leave_managment(
            reason=reason,
            from_date=from_date,
            to_date=to_date,
            emp_id=emp_id,
            leave_status=status,
        )
        print("from_date: ", from_date)

        try:
            db.session.add(new_leave)
            print("new_leave added: ", new_leave)
            db.session.commit()
        except sqlalchemy.exc.DataError as e:
            return jsonify(
                {"err": "Data Error occured. Date format must be in YYYY-MM-DD"}
            )
        except Exception as e:
            return jsonify({"err": str(e)})

        return jsonify({"msg": "Leave request sent!"}), 200
    else:
        return jsonify({"msg": "User not found!"}), 404

