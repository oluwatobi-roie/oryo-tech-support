




oryo-tech-platform/
│── user_service/        # User Management (Flask)
│   ├── app/
│   │   ├── models.py
│   │   ├── routes.py
│   │   ├── services.py
│   │   ├── __init__.py
│   ├── config.py
│   ├── requirements.txt
│   ├── run.py
│   ├── Dockerfile
│── task_service/        # Task Management (Django)
│── vehicle_service/     # Vehicle Management (Django)
│── notification_service/ # Notifications (Flask)
│── api_gateway/         # API Gateway (Flask or Nginx)
│── docker-compose.yml   # To orchestrate microservices
│── .env                 # Environment variables
