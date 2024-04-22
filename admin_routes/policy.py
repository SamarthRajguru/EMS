from datetime import datetime
from flask import Blueprint, request, jsonify
from create_app import db
from auth import token_required, role_required
from models import Policy


policy_bp = Blueprint("policy_bp", __name__)


@policy_bp.route("/create")
@token_required
@role_required("1")
def create_policy():
    data = request.get_json()
    description = data.get("description")
    date_created = datetime.now()
    print("date_created :", date_created)

    if description:
        new_policy = Policy(description=description, date_created=date_created)

        try:
            db.session.add(new_policy)
            db.session.commit()
            return jsonify({"msg": "Policy added"})
        except Exception as e:
            return jsonify({"err": str(e)})
    else:
        return jsonify({"msg": "Invalid Description"})


@policy_bp.route("/update")
@token_required
@role_required("1")
def update_policy():
    id = request.args.get("id")
    data = request.get_json()
    description = data.get("description")
    date_created = datetime.now()

    update_policy = db.session.query(Policy).filter(Policy.id == id).first()
    print("Updated Policy", description)
    update_policy.description = description
    update_policy.date_created = date_created

    try:
        db.session.commit()
        return jsonify({"msg": "Description Updated Successfuly"})
    except Exception as e:
        return jsonify({"err": str(e)})


@policy_bp.route("/delete")
@token_required
@role_required("1")
def delete_policy():
    policy_id = request.args.get("id", type=int)
    policy = db.session.query(Policy).filter(Policy.id == policy_id).first()
    if policy:
        try:
            db.session.delete(policy)
            db.session.commit()
            return jsonify({"msg": "Policy Revoked"}), 200

        except Exception as e:
            return jsonify({"msg": str(e)}), 500
    else:
        return jsonify({"msg": "Policy not found"}), 404


@policy_bp.route("/get/all")
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
