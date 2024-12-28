from db.setup_db import db

class Result(db.Model):
    __tablename__ = 'results'

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100), nullable=False)  # Firstname, Lastname
    answers = db.Column(db.String(255), nullable=False)  # Store comma-separated answers (e.g., "A,C")
    total_points = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(100), nullable=False)  # Store quiz category
    is_deleted = db.Column(db.Boolean, default=False)
    is_updated = db.Column(db.Boolean, default=False)

    @staticmethod
    def save_result(user_name, answers, total_points, category):
        """Save quiz result for a user."""
        result = Result(user_name=user_name, answers=answers, total_points=total_points, category=category)
        db.session.add(result)
        db.session.commit()
        return result

    # @staticmethod
    # def get_user_result(user_name):
    #     """Get the result for a specific user."""
    #     return Result.query.filter_by(user_name=user_name, is_deleted=False).all()

    @staticmethod
    def get_user_result(user_name):
        """Get the result for a specific user."""
        results = Result.query.filter_by(user_name=user_name, is_deleted=False).all()
        for result in results:
            # Convert answers to an array
            result.answers = result.answers.split(',')  # Split the comma-separated string into a list
        return results

    @staticmethod
    def get_all_results():
        """Get all results (admin access)."""
        return Result.query.filter_by(is_deleted=False).all()
