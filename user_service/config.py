# config.py
import os

class Config:
    SECRET_KEY = "e72ace4959a704699dc3cd7b1d4212d7" # Change this in production
    SQLALCHEMY_DATABASE_URI = "postgresql://devenv:devpassword@localhost:5432/oryodb"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your_jwt_secret_key")  # Change this in production
