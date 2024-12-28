from datetime import timedelta



import app


class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:prajwal@localhost/sampledatabase'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '48791f09101f934b418df925f54759cc0a6f5950d38cbc248b860f8ba42255f7'  # Replace with a secure key
    JWT_SECRET_KEY = '77810d9c59f953cea439ef36152879bb48ddb06668f082ac293e4b87f275a833'  # Replace with a secure key
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_ERROR_MESSAGE_KEY = 'message'

    # Additional database configuration
    SQLALCHEMY_ECHO = True  # Log SQL queries (set to False in production)
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_timeout': 30,
        'pool_recycle': 1800,  # Recycle connections after 30 minutes
    }

