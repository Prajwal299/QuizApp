4# controllers/token_controller.py
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from flask_restful import Resource
from flask import jsonify

class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        """
        Endpoint for refreshing access tokens using a valid refresh token.
        """
        try:
            # Get the current user identity
            current_user_id = get_jwt_identity()

            if not current_user_id:
                return {"message": "Invalid user identity"}, 401

            # Create new access token
            new_access_token = create_access_token(identity=current_user_id)

            return {
                "access_token": new_access_token,
                "message": "Token refreshed successfully"
            }, 200

        except Exception as e:
            print(f"Token refresh error: {str(e)}")
            return {"message": "Error refreshing token"}, 500