# controllers/user_controller.py
import logging

from db.setup_db import db
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token, jwt_required, get_jwt_identity,
)

from flask_restful import Resource
from flask import request, jsonify

from models.result_model import Result
from models.user_model import User

from werkzeug.security import generate_password_hash, check_password_hash


class UserRegistration(Resource):
    def post(self):
        data = request.get_json()
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        password = data.get('password')
        is_admin = data.get('is_admin', False)  # Default to False if not provided

        # Validate required fields
        if not first_name or not last_name or not email or not password:
            return {"msg": "All fields are required"}, 400

        # Check if the user already exists
        if User.find_by_email(email):
            return {"msg": "User already exists"}, 409

        # Hash the password before storing it
        hashed_password = generate_password_hash(password)

        # Create new user
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=hashed_password,  # Store hashed password
            is_admin=is_admin
        )
        db.session.add(new_user)
        db.session.commit()

        return {"msg": "User registered successfully"}, 201



class UserLogin(Resource):
    def post(self):
        try:
            # Get and validate request data
            data = request.get_json()
            if not data:
                return {"message": "No data provided"}, 400

            email = data.get('email')
            password = data.get('password')

            # Validate required fields
            if not email or not password:
                return {
                    "message": "Missing required fields",
                    "errors": {
                        "email": "Required" if not email else None,
                        "password": "Required" if not password else None
                    }
                }, 400

            # Find user and verify credentials
            user = User.find_by_email(email)
            if not user:
                return {"message": "Invalid email or password"}, 401

            if not check_password_hash(user.password, password):
                return {"message": "Invalid email or password"}, 401

            # Generate tokens
            access_token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(identity=user.id)

            # Return success response with user details (including first_name and last_name)
            return {
                "message": "Login successful",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "first_name": user.first_name,  # Include first_name
                    "last_name": user.last_name,  # Include last_name
                    "is_admin": user.is_admin
                },
                "access_token": access_token,
                "refresh_token": refresh_token
            }, 200

        except Exception as e:
            return {"message": "An unexpected error occurred", "error": str(e)}, 500


class UserResult(Resource):
    @jwt_required()
    def get(self, user_name):
        user_results = Result.get_user_result(user_name)  # Get results for the user by user_name

        if not user_results:
            return {"message": "No results found for this user"}, 404

        results = [
            {
                "id": result.id,
                "user_name": result.user_name,
                "total_points": result.total_points,
                "category": result.category,
                "answers": result.answers
            } for result in user_results
        ]

        return results, 200


class AdminResults(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()  # Get the user ID from the JWT token
        # Assuming the user is an admin, you can add authorization checks here
        # For now, let's allow access to all results for the sake of simplicity
        if not is_admin(user_id):
            return {"message": "You are not authorized to view all results"}, 403

        all_results = Result.get_all_results()  # Get all results for admin

        results = [
            {
                "id": result.id,
                "user_name": result.user_name,
                "total_points": result.total_points,
                "category": result.category,
                "answers": result.answers
            } for result in all_results
        ]

        return results, 200


# Helper function to check if the user is an admin
def is_admin(user_id):
    # Replace with actual logic to check if the user is an admin
    user = User.query.get(user_id)
    return user.is_admin if user else False