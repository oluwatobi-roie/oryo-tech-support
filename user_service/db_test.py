from app.models import db
from run import app
from sqlalchemy import text

with app.app_context():
    try:
        db.session.execute(text("SELECT 1"))
        print("Database connected successfully!")
    except Exception as e:
        print(f"Database connection failed: {e}")