from flask_sqlalchemy import SQLAlchemy

# Create an instance of SQLAlchemy
db = SQLAlchemy()


def init_db(app):
    """Initialize the app with the database and create tables if they don't exist"""
    db.init_app(app)

    # Create all tables within application context
    with app.app_context():
        # Import all models here to ensure they are known to SQLAlchemy
        from models.user_model import User  # Import other models as needed

        # Create tables if they don't exist
        db.create_all()
