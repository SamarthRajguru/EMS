import random
import string
from flask import Blueprint, request, jsonify
from create_app import app, db, mail, bcrypt
from models import Employee
from flask_mail import Mail, Message

forgot_pass_bp = Blueprint("forgot_pass_bp", __name__)


@forgot_pass_bp.route("/password", methods=["POST"])
def forgot_password():
    data = request.get_json()
    email = data.get("email")
    user = db.session.query(Employee).filter(Employee.email == email).first()

    if user:
        # Generate a new random password
        new_password = "".join(
            random.choices(string.ascii_letters + string.digits, k=8)
        )

        # encryption of password using bcrypt before commiting to database
        hashed_password = bcrypt.generate_password_hash(new_password).decode("utf-8")

        user.password = hashed_password
        db.session.commit()

        msg = Message(
            "New Password", sender="your_email@example.com", recipients=[email]
        )
        msg.body = f"Dear Employee, \n\n\t\tYour password has been reset successfully. Below is your new password. \n\t\tNew Password: {new_password} \n\t\tFor security reasons, we recommend changing your password after logging in. \n\nThank you \nAlcyone Technologies"
        mail.send(message=msg)
        return jsonify({"msg": "Email sent to your mail"})

    else:
        return jsonify({"msg": "Email not found, Please Register first..."})
