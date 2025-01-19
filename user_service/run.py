from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from app.models import db, User, RoleEnum  # Ensure correct import
from app.routes import user_bp

def create_app(config_object='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_object)

    # Initialize extensions
    db.init_app(app)
    jwt = JWTManager(app)
    migrate = Migrate(app, db)  # Ensure Migrate is initialized here

    app.register_blueprint(user_bp, url_prefix='/users')

    with app.app_context():
    #Check if the admin user already exists
        if not User.query.filter_by(email="oluwatobi.akomolafe@oryoltd.com").first():
            # Create a default admin user
            admin_user = User(
                f_name="Oluwatobi",
                l_name="Akomolafe",
                email="oluwatobi.akomolafe@oryoltd.com",
                phone_number="07037870700",
                role=RoleEnum.GENERAL_ADMIN,
                department="Admin",  # Add appropriate department if needed
            )
            admin_user.set_password("12345")
            db.session.add(admin_user)
            db.session.commit()
            print("Default user for Oluwatobi.akomolafe set")

        print("Default user exist... Continuing application")

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
