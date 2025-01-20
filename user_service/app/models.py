# user_service/app/models.py
# Models available here are
#  User (for registering all users)
#  Client (This houses all clients associated with Oryo0)
#  Projects (This table describe all project and what is required of the project)
# InstallationTask (This is the list of installations required)

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import enum
from sqlalchemy.dialects.postgresql import JSON

db = SQLAlchemy()

class RoleEnum(enum.Enum):
    GENERAL_ADMIN = "General Admin"
    MANAGEMENT = "Management"
    TECH_SUPPORT = "Technical Support"
    ON_SITE_TECHNICIAN = "On-Site Technician"

class User(db.Model):
    __tablename__ = 'users' #Explicitly specify table name to avoid reserved keyword in postgresql conflict
    id = db.Column(db.Integer, primary_key=True)
    f_name= db.Column(db.String(80), nullable=False)
    l_name = db.Column(db.String(80), nullable=False)
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


class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    address = db.Column(db.String(255), nullable=True)
    project_manager = db.Column(db.String(255), nullable=True)
    
    projects = db.relationship('Project', backref='client', lazy=True)



class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    po_number = db.Column(db.String(100), unique=True, nullable=False)
    
    installation_tasks = db.relationship('InstallationTask', backref='project', lazy=True)



class InstallationTask(db.Model):
    __tablename__ = 'installation_tasks'
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    product_type = db.Column(db.String(255), nullable=False)
    assigned_technician_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    status = db.Column(db.String(50), default='Pending')  # Possible values: Pending, In Progress, Awaiting Approval, Completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    additional_data = db.Column(JSON, nullable=True)  # Store product-specific data dynamically
    
    technician = db.relationship('User', backref='installation_tasks', lazy=True)
