# user_service/app/models.py
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import enum
from sqlalchemy.dialects.postgresql import JSON

db = SQLAlchemy()

class RoleEnum(enum.Enum):
    GENERAL_ADMIN = "General Admin"
    MANAGEMENT = "Management"
    TECH_SUPPORT = "Technical Support"
    ON_SITE_TECHNICIAN = "On-Site Technician"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.Enum(RoleEnum), nullable=False)
    permissions = db.Column(JSON, nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}, Role: {self.role.value}>"
