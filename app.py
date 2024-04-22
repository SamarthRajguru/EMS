from create_app import app
from admin_routes.home import home_bp
from user_routes.login import login_bp
from admin_routes.employee import employee_bp
from admin_routes.role import role_bp
from admin_routes.leave import leave_bp
from admin_routes.policy import policy_bp
from user_routes.attendance import attendance_bp
from user_routes.forgot_password import forgot_pass_bp
from user_routes.user_routes import user_routes_bp

print("working")
app.register_blueprint(home_bp, url_prefix="/home")

app.register_blueprint(login_bp, url_prefix="/login")

app.register_blueprint(employee_bp, url_prefix="/employee")

app.register_blueprint(role_bp, url_prefix="/role")

app.register_blueprint(leave_bp, url_prefix="/leave")

app.register_blueprint(policy_bp, url_prefix="/policy")

app.register_blueprint(attendance_bp, url_prefix="/attendance")

app.register_blueprint(forgot_pass_bp, url_prefix="/forgot")

app.register_blueprint(user_routes_bp, url_prefix="/user")


if __name__ == "__main__":
    app.run(debug=True)
