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

    # Register blueprints
    from restful_api import restful_api_bp
    app.register_blueprint(restful_api_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)