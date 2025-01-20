from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS #Importing cross origin region enablement
from flask_jwt_extended import JWTManager
from app.models import db, User, RoleEnum  # Ensure correct import
from app.routes import user_bp
from app.tech_support import tech_support_bp


def create_app(config_object='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_object)
    CORS(app, resources={r"/*":{ "origins": "*"}})

    # Initialize extensions
    db.init_app(app)
    jwt = JWTManager(app)
    migrate = Migrate(app, db)  # Ensure Migrate is initialized here



    # Importing necessary Routes for the API
    app.register_blueprint(user_bp, url_prefix='/users')
    app.register_blueprint(tech_support_bp, url_prefix='/tech_support')






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
        
        if not User.query.filter_by(email="tech.support@oryoltd.com").first():
            # Create a default admin user
            admin_user = User(
                f_name="Technical",
                l_name="Support",
                email="tech.support@oryoltd.com",
                phone_number="07037870700",
                role=RoleEnum.TECH_SUPPORT,
                department="Technical Support",  # Add appropriate department if needed
            )
            admin_user.set_password("12345")
            db.session.add(admin_user)
            db.session.commit()
            print("Default tech_support User for tech.support@oryoltd.com set")

        if not User.query.filter_by(email="site.technician@oryoltd.com").first():
            # Create a default admin user
            admin_user = User(
                f_name="Onsite",
                l_name="Technician",
                email="site.technician@oryoltd.com",
                phone_number="07037870700",
                role=RoleEnum.ON_SITE_TECHNICIAN,
                department="Abuja Technician",  # Add appropriate department if needed
            )
            admin_user.set_password("12345")
            db.session.add(admin_user)
            db.session.commit()
            print("Default onsite technician user for site.technician@oryoltd.com set")

        print("Default users exist... Continuing application")

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
