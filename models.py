from datetime import datetime
from create_app import db, app


class Employee(db.Model):
    __tablename__ = "employee_details"
    emp_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey("role.role_id"), nullable=False)
    role = db.relationship("Role", backref=db.backref("employees", lazy=True))
    name = db.Column(db.String(50))
    contact = db.Column(db.BigInteger)
    leaves = db.Column(db.Integer, default=0)
    on_boarding = db.Column(db.Date, default=datetime.today().date())

    def __repr__(self):
        return f"<Employee ID = {self.emp_id}, Employee name = {self.name}>"

    print("Employee Table called")


class Role(db.Model):
    __tablename__ = "role"
    role_id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(50), unique=True, nullable=False)

    print("Roles table called")


class Leave_managment(db.Model):
    __tablename__ = "leave_managment"

    leave_id = db.Column(db.Integer, primary_key=True)
    reason = db.Column(db.String(1000), nullable=False)
    from_date = db.Column(db.DateTime, nullable=False)
    to_date = db.Column(db.DateTime, nullable=False)
    leave_status = db.Column(db.String(15), default="Pending")
    emp_id = db.Column(
        db.Integer, db.ForeignKey("employee_details.emp_id"), nullable=False
    )
    role = db.relationship("Employee", backref=db.backref("assigned_leaves", lazy=True))

    print("Leave table called")


class Policy(db.Model):
    __tablename__ = "policies"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(2000))
    date_created = db.Column(db.DateTime, default=datetime.today().timestamp)

    print("Policy Table called")


class Attendance(db.Model):
    __tablename__ = "employee_attendance"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.today().date())

    present = db.Column(db.Boolean, default=False)
    on_halfday = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(55))
    emp_id = db.Column(
        db.Integer, db.ForeignKey("employee_details.emp_id"), nullable=False
    )

    print("Attendance Table called")


with app.app_context():
    db.create_all()
    db.session.commit()
