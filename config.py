from datetime import timedelta



import app


class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:prajwal@localhost/sampledatabase'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '5a79b562a64eca1f555a47dd24b6fdb725b452b2fae7b97d9f3a67464b64ce73'  # Replace with a secure key
    JWT_SECRET_KEY = '1f639bb21f6c9861b4fd775d0238f4e1a01799d06f638bd8d2be582e83ce6c2a'  # Replace with a secure key
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_ERROR_MESSAGE_KEY = 'message'

    # Additional database configuration
    # SQLALCHEMY_ECHO = True  # Log SQL queries (set to False in production)
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_timeout': 30,
        'pool_recycle': 1800,  # Recycle connections after 30 minutes
    }

