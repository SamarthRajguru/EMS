from flask import Blueprint, request, jsonify
from create_app import bcrypt, db
from models import Employee
from auth import token_required, role_required
import psycopg2
import sqlalchemy


employee_bp = Blueprint("employee_bp", __name__)


@employee_bp.route("/create", methods=["POST"])
@token_required
@role_required("1")
def create_user():
    data = request.get_json()
    local_email = data.get("email")
    local_password = data.get("password")
    local_name = data.get("name")
    local_contact = data.get("contact")
    role_id = data.get("role_id")
    hashed_password = bcrypt.generate_password_hash(local_password).decode("utf-8")

    new_user = Employee(
        email=local_email,
        password=hashed_password,
        name=local_name,
        contact=local_contact,
        role_id=role_id,
    )
    try:
        db.session.add(new_user)
        db.session.commit()
        print(f"User {new_user.name} added...")
        return jsonify(f"User {new_user.name} added...")
    except psycopg2.errors.UniqueViolation:
        return jsonify({"Error": "Unique Voilation"})
    except sqlalchemy.exc.IntegrityError as err:
        print(err)
        e = {"Error": print(err)}
        return jsonify({"Error": "Integrity Error due to redundancy"}), 404


@employee_bp.route("/delete", methods=["DELETE"])
@token_required
@role_required("1")
def delete():
    data = request.get_json()
    id = data.get("emp_id")

    user = db.session.query(Employee).filter(Employee.emp_id == id).first()

    if user:

        name = user.name
        db.session.delete(user)
        db.session.commit()

        return jsonify({"Message": "User " + name + " deleted successfully..."})
    else:
        return jsonify({"Message": "User not found"}), 404


@employee_bp.route("/get/all", methods=["GET"])
@token_required
@role_required("1")
def retrive_all():

    page_no = request.args.get("page_no", default=1, type=int)
    per_page = request.args.get("per_page", default=5, type=int)

    if page_no < 1:
        return jsonify({"mesage": "Invalid Page \n Page number starts from 1"})
    else:
        offset = (page_no - 1) * per_page
        total_count = db.session.query(Employee).count()
        items = db.session.query(Employee).offset(offset).limit(per_page).all()

        users_list = []

        for user in items:
            user_dict = {
                "id": user.emp_id,
                "name": user.name,
                "email": user.email,
                "contact": user.contact,
                "role": user.role_id,
            }
            users_list.append(user_dict)

            print("user_list : ", users_list)
        print("total_count : ", total_count)
        print("pets : ", items)

        response = {
            "total_count": total_count,
            "page": page_no,
            "per_page": per_page,
            "pets": users_list,
        }

        return jsonify(response)
