# Directory: user_service/app/routes.py
# routes available here are
# Register Route
# Login Route

from flask import Blueprint, json, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from .models import db, User, RoleEnum

user_bp = Blueprint('user_bp', __name__)


# Register New user Route
@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    required_fields = ['f_name', 'l_name', 'email', 'password', 'role']
    # Handle if all data is not complete first, alternatively will be to set this up from the front end
    if not data or not all(k in data for k in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    # handle if user already exist
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "User already exists"}), 400

    role = data["role"].strip().title()
    if role not in [r.value for r in RoleEnum]:
        return jsonify({"error": "Invalid role provided"}), 400

    new_user = User(
        f_name=data["f_name"],
        l_name=data["l_name"],
        email=data["email"],
        department=data.get("department", "Unknown"),  # Default department if not provided
        phone_number=data.get("phone_number", ""),
        role=RoleEnum[role.replace(" ", "_").upper()]
    )
    new_user.set_password(data["password"])

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201




@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not all(k in data for k in ("email", "password")):
        return jsonify({"error": "Missing required fields"}), 400

    user = User.query.filter_by(email=data["email"]).first()
    if not user or not user.check_password(data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    
    identity_data = json.dumps({
        "id": user.id,
        "role": user.role.value,
        "email": user.email,
        "department": user.department  # Add any other fields here
    })
    access_token = create_access_token(identity=identity_data)
    return jsonify({"access_token": access_token}), 200
    # access_token = create_access_token(identity={"id": user.id, "role": user.role.value})
    # return jsonify({"access_token": access_token}), 200



@user_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify({"message": f"Hello {current_user['id']}, you have access!"}), 200





@user_bp.route('/test', methods=['GET'])
def test():
    return jsonify({"message": "CORS is working!"})