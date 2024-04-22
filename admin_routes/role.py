from flask import Blueprint, request, jsonify
from auth import token_required, role_required
from create_app import db
from models import Role

role_bp = Blueprint("role_bp", __name__)


@role_bp.route("/create", methods=["POST"])
@token_required
@role_required("1")
def create_role():
    data = request.get_json()
    role = data.get("role")
    if role:
        new_role = Role(role=role)

        try:
            db.session.add(new_role)
            db.session.commit()
        except Exception as e:
            print(str(e))
            return jsonify({"err": str(e)})
        return jsonify({"msg": "Roled Added"})


@role_bp.route("/get", methods=["GET"])
@token_required
@role_required("1")
def get_role():
    role_id = request.args.get("role_id", type=int)

    if role_id:
        try:
            role = db.session.query(Role).filter(Role.role_id == role_id).first()

        except Exception as e:
            return str(e)
        return jsonify({"role_id": role.role_id, "role": role.role})
    else:
        return jsonify({"msg": "Role not Found"}), 404


@role_bp.route("/get/all", methods=["GET"])
@token_required
@role_required("1")
def retrive_all():

    page_no = request.args.get("page_no", default=1, type=int)
    per_page = request.args.get("per_page", default=5, type=int)

    if page_no < 1:
        return jsonify({"mesage": "Invalid Page \n Page number starts from 1"})
    else:
        offset = (page_no - 1) * per_page
        total_count = db.session.query(Role).count()
        items = db.session.query(Role).offset(offset).limit(per_page).all()

        users_list = []

        for user in items:
            user_dict = {
                "role_id": user.role_id,
                "role": user.role,
            }
            users_list.append(user_dict)

            print("user_list : ", users_list)
        print("total_count : ", total_count)
        print("user : ", items)

        response = {
            "total_count": total_count,
            "page": page_no,
            "per_page": per_page,
            "pets": users_list,
        }

        return jsonify(response)


@role_bp.route("/delete", methods=["DELETE"])
@token_required
@role_required("1")
def delete_role():
    role_id = request.args.get("role_id", type=int)

    delete_role = db.session.query(Role).filter(Role.role_id == role_id).first()
    print("Deleted Role", delete_role)

    try:
        db.session.delete(delete_role)
        db.session.commit()
    except Exception as e:
        return jsonify({"err": str(e)})
    return jsonify({"msg": "Role deleted"})


@role_bp.route("/update", methods=["PUT"])
@token_required
@role_required("1")
def update_role():
    role_id = request.args.get("role_id", type=int)
    data = request.get_json()
    role = data.get("role")

    update_role = db.session.query(Role).filter(Role.role_id == role_id).first()
    print("Updated Role", delete_role)
    update_role.role = role
    try:
        db.session.commit()
    except Exception as e:
        return jsonify({"err": str(e)})
    return jsonify({"msg": "Role updated"})
