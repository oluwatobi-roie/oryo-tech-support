# user_service/run.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from app.routes import user_bp

# Initialize extensions
db = SQLAlchemy()
jwt = JWTManager()


def create_app(config_object='config.Config'):
    app = Flask(__name__)

    # Load configuration from the config.py file
    app.config.from_object(config_object)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)

    # Register blueprints for the user routes
    app.register_blueprint(user_bp, url_prefix='/users')

    # Create all tables if needed (use migrations in production)
    with app.app_context():
        db.create_all()

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)