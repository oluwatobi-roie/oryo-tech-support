
Setup Postgres SQL
login to your postgres SQL machine and set the set the following
# Create database
    CREATE DATABASE companydb
# Create User
    CREATE USER username WITH PASSWORD 'password'

in your Config.py file
Update the SQLALCHEMY_DATABASE_URI
    SQLALCHEMY_DATABASE_URI = "postgresql://username_set:password_set@hostaddress:5432/companydb"

its advisable to restart your psql server,
in windows you can use the following command
    net stop postgresql-x64-17
    net start postgresql-x64-17
Don't forget to update the version of the psql server you are running on, as I am currently running on versino 17

# Initiailizing your database from flask app
    1. navigate to the virtual enviroment for your application,
    2. set enviromental variable as: 
            $env:FLASK_APP = "user_service/run.py"
    3. Verify enviromental variable is pointing to the root of your application, in my case it is run.py
            echo $env:FLASK_APP
        this should return user_service/run.py
    4. run the initilization of your db


# Grant Priviledges to the psql users 
-- Switch to the correct database
\c oryodb

-- Give full access to the database user
ALTER USER devenv WITH SUPERUSER;

-- OR (safer) Grant specific privileges instead of superuser
GRANT ALL PRIVILEGES ON DATABASE oryodb TO devenv;
GRANT ALL PRIVILEGES ON SCHEMA public TO devenv;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO devenv;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO devenv;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON FUNCTIONS TO devenv;





oryo-tech-platform/
│── user_service/        # User Management (Flask)
│   ├── app/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   ├── services.py
│   │   ├── models.py
│   ├── __init__.py #deleted
│   ├── .gitignore
│   ├── config.py
│   ├── requirements.txt
│   ├── run.py
│   ├── Dockerfile
│── task_service/        # Task Management (Django)
│── vehicle_service/     # Vehicle Management (Django)
│── notification_service/ # Notifications (Flask)
│── api_gateway/         # API Gateway (Flask or Nginx)
│── docker-compose.yml   # To orchestrate microservices

