from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql://postgres:root@localhost:5432/Employee_Managment_System"
)
app.config["SECRET_KEY"] = "secret"

app.config["MAIL_SERVER"] = "smtp.gmail.com"  # this is my SMTP server
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "samarthrajguru2@gmail.com"  # Change this to your email
app.config["MAIL_PASSWORD"] = "Password"  # Change this to your email password

mail = Mail(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
