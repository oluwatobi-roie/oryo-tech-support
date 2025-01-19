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
    __tablename__ = 'users' #Explicitly specify table name to avoide reservfed keyword in postgresql conflict
    id = db.Column(db.Integer, primary_key=True)
    f_name= db.Column(db.String(80), unique=True, nullable=False)
    l_name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    department = db.Column(db.String(80), nullable=False)
    phone_number = db.Column(db.String(16), nullable=False)
    role = db.Column(db.Enum(RoleEnum), nullable=False)
    permissions = db.Column(JSON, nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}, Role: {self.role.value}>"
