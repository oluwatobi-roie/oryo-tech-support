# Directory: user_service/app/gen_admin.py
#Routes available are
#  Client Routes [GET, POST, PUT, DELETE]
#  Projects Routes [GET, POST, PUT, DELETE]
#  User Routes [GET, POST, PUT, DELETE]



from flask import Blueprint, request, jsonify, json
from app.models import db, User, Client, Project, RoleEnum
from flask_jwt_extended import jwt_required, get_jwt_identity


admin_bp = Blueprint('admin', __name__)


def is_general_admin():
    """Check if the logged-in user is a General Admin."""
    current_user = get_jwt_identity()

    # Deserialize the 'sub' field, since it's a stringified JSON object
    current_user = json.loads(current_user)

    print("\n\n\n\n\n\n\n\nWe are exploring gen admin Route\n\n\n\n\n\n\n\n")
    print(current_user)

    # Now you have the user data as a dictionary, access the role
    return current_user and current_user.get("role") == "General Admin"




# ----------- CLIENT ROUTES -----------
@admin_bp.route('/clients', methods=['GET'])
@jwt_required()
def get_clients():
    """Retrieve all clients"""
    print("Debug Comment: we are in client GET api")
    if not is_general_admin():
        return jsonify({"message": "Unauthorized"}), 403

    clients = Client.query.all()
    return jsonify([{"id": c.id, "name": c.name, "email": c.email, "address": c.address, "project_manager": c.project_manager} for c in clients])


@admin_bp.route('/clients', methods=['POST'])
@jwt_required()
def create_client():
    """Create a new client"""
    if not is_general_admin():
        return jsonify({"message": "Unauthorized"}), 403

    data = request.json
    print("\n\n\n\n\n\nHere is UserData: ", data)
    new_client = Client(name=data["name"], email=data["email"], address=data.get("address"), project_manager=data.get("project_manager"))
    db.session.add(new_client)
    db.session.commit()
    return jsonify({"message": "Client created successfully"}), 201


@admin_bp.route('/clients/<int:client_id>', methods=['PUT'])
@jwt_required()
def update_client(client_id):
    """Update client details"""
    if not is_general_admin():
        return jsonify({"message": "Unauthorized"}), 403

    client = Client.query.get(client_id)
    if not client:
        return jsonify({"message": "Client not found"}), 404

    data = request.json
    client.name = data.get("name", client.name)
    client.email = data.get("email", client.email)
    client.address = data.get("address", client.address)
    client.project_manager = data.get("project_manager", client.project_manager)

    db.session.commit()
    return jsonify({"message": "Client updated successfully"})



@admin_bp.route('/clients/<int:client_id>', methods=['DELETE'])
@jwt_required()
def delete_client(client_id):
    """Delete a client"""
    if not is_general_admin():
        return jsonify({"message": "Unauthorized"}), 403

    client = Client.query.get(client_id)
    if not client:
        return jsonify({"message": "Client not found"}), 404

    db.session.delete(client)
    db.session.commit()
    return jsonify({"message": "Client deleted successfully"})






# ----------- PROJECT ROUTES -----------
@admin_bp.route('/projects', methods=['GET'])
@jwt_required()
def get_projects():
    """Retrieve all projects"""
    if not is_general_admin():
        return jsonify({"message": "Unauthorized"}), 403

    projects = Project.query.all()
    return jsonify([{"id": p.id, "description": p.description, "client_id": p.client_id, "po_number": p.po_number} for p in projects])

@admin_bp.route('/projects', methods=['POST'])
@jwt_required()
def create_project():
    """Create a new project"""
    if not is_general_admin():
        return jsonify({"message": "Unauthorized"}), 403

    data = request.json
    new_project = Project(description=data["description"], client_id=data["client_id"], po_number=data["po_number"])
    db.session.add(new_project)
    db.session.commit()
    return jsonify({"message": "Project created successfully"}), 201

@admin_bp.route('/projects/<int:project_id>', methods=['PUT'])
@jwt_required()
def update_project(project_id):
    """Update project details"""
    if not is_general_admin():
        return jsonify({"message": "Unauthorized"}), 403

    project = Project.query.get(project_id)
    if not project:
        return jsonify({"message": "Project not found"}), 404

    data = request.json
    project.description = data.get("description", project.description)
    project.client_id = data.get("client_id", project.client_id)
    project.po_number = data.get("po_number", project.po_number)

    db.session.commit()
    return jsonify({"message": "Project updated successfully"})

@admin_bp.route('/projects/<int:project_id>', methods=['DELETE'])
@jwt_required()
def delete_project(project_id):
    """Delete a project"""
    if not is_general_admin():
        return jsonify({"message": "Unauthorized"}), 403

    project = Project.query.get(project_id)
    if not project:
        return jsonify({"message": "Project not found"}), 404

    db.session.delete(project)
    db.session.commit()
    return jsonify({"message": "Project deleted successfully"})





# ----------- USER ROUTES -----------
@admin_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    """Retrieve all users"""
    if not is_general_admin():
        return jsonify({"message": "Unauthorized"}), 403

    users = User.query.all()
    return jsonify([{"id": u.id, "f_name": u.f_name, "l_name": u.l_name, "email": u.email, "role": u.role.value} for u in users])

@admin_bp.route('/users', methods=['POST'])
@jwt_required()
def create_user():
    """Create a new user"""
    if not is_general_admin():
        return jsonify({"message": "Unauthorized"}), 403
    
    data = request.json
    new_user = User(
        f_name=data["f_name"],
        l_name=data["l_name"],
        email=data["email"],
        department=data["department"],
        phone_number=data["phone_number"],
        role=RoleEnum(data.get('role')).name,
    )
    new_user.set_password(data["password"])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully"}), 201


@admin_bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    """Update user details"""
    if not is_general_admin():
        return jsonify({"message": "Unauthorized"}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    data = request.json
    user.f_name = data.get("f_name", user.f_name)
    user.l_name = data.get("l_name", user.l_name)
    user.email = data.get("email", user.email)
    user.department = data.get("department", user.department)
    user.phone_number = data.get("phone_number", user.phone_number)
    user.role = RoleEnum[data.get("role", user.role.name)]

    db.session.commit()
    return jsonify({"message": "User updated successfully"})



@admin_bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    """Delete a user"""
    if not is_general_admin():
        return jsonify({"message": "Unauthorized"}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"})
