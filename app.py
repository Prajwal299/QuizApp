# from flask import Flask
# from config import Config
# from db.setup_db import init_db
# from flask_jwt_extended import JWTManager
#
#
# def create_app():
#     app = Flask(__name__)
#     app.config.from_object(Config)
#
#     # Initialize database
#     init_db(app)
#
#     # Initialize JWT
#     jwt = JWTManager(app)
#
#     # Register blueprints
#     from restful_api import restful_api_bp
#     app.register_blueprint(restful_api_bp)
#
#     return app
#
# if __name__ == '__main__':
#     app = create_app()
#     app.run(debug=True)


# app.py
from flask import Flask
from config import Config
from db.setup_db import init_db
from flask_jwt_extended import JWTManager
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

    # Initialize database
    init_db(app)

    # Initialize JWT Manager
    jwt = JWTManager(app)

    # JWT callback handlers
    @jwt.user_identity_loader
    def user_identity_lookup(user):
        # Convert user identity to string when creating tokens
        return str(user) if user is not None else None

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        # Look up user from database when verifying tokens
        from models.user_model import User
        identity = jwt_data["sub"]
        return User.query.filter_by(id=identity).one_or_none()

    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        # You can implement token blocklist checking here
        # For now, just return False (no tokens are blocked)
        return False

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return {
            "message": "The token has expired",
            "error": "token_expired"
        }, 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return {
            "message": "Signature verification failed",
            "error": "invalid_token"
        }, 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return {
            "message": "Request does not contain an access token",
            "error": "authorization_required"
        }, 401

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return {
            "message": "The token is not fresh",
            "error": "fresh_token_required"
        }, 401

    # Register blueprints
    from restful_api import restful_api_bp
    app.register_blueprint(restful_api_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)