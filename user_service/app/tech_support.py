from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, InstallationTask, User

tech_support_bp = Blueprint('tech_support', __name__)

TaskStatus = "awaiting"

@tech_support_bp.route('/tasks/create', methods=['POST'])
@jwt_required()
def create_task():
    data = request.get_json()
    current_user = get_jwt_identity()
    
    # Ensure current user is Tech Support
    user = User.query.get(current_user['id'])
    role = User.query.get(current_user['role'])

    if not user or role != 'Technical Support':
        return jsonify({'error': 'Unauthorized'}), 403

    new_task = InstallationTask(
        project_id=data['project_id'],
        assigned_technician_id=data['technician_id'],
        product_type=data['product_type'],
        # task_status=TaskStatus.NEW,
        task_data=data['task_data']  # JSON data specific to product type
    )
    db.session.add(new_task)
    db.session.commit()

    return jsonify({'message': 'Task created successfully'}), 201



@tech_support_bp.route('/tasks/awaiting_confirmation', methods=['GET'])
@jwt_required()
def get_awaiting_confirmation_tasks():
    tasks = InstallationTask.query.filter_by(task_status=TaskStatus.AWAITING_CONFIRMATION).all()
    return jsonify([task.to_dict() for task in tasks]), 200




@tech_support_bp.route('/tasks/confirm/<int:task_id>', methods=['POST'])
@jwt_required()
def confirm_task(task_id):
    data = request.get_json()
    task = InstallationTask.query.get(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404

    if data['status'] == 'approved':
        task.task_status = TaskStatus.COMPLETED
    elif data['status'] == 'returned':
        task.task_status = TaskStatus.RETURNED
    else:
        return jsonify({'error': 'Invalid status'}), 400

    db.session.commit()
    return jsonify({'message': 'Task status updated successfully'}), 200
