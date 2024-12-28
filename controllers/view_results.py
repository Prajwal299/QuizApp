from datetime import datetime, timedelta

from flask_restful import Resource
from flask import request, jsonify
from sqlalchemy.exc import SQLAlchemyError

from models.advance_model import Category, paginate_query, QuizHistory, Leaderboard
from models.result_model import Result
from models.question_model import Question
from db.setup_db import db

class QuestionList(Resource):
    def get(self, category):
        questions = Question.get_all_by_category(category)
        if not questions:
            return {"message": "No questions found"}, 404
        return jsonify([{
            "id": q.id,
            "question": q.question,
            "options": {
                'A': q.option_a,
                'B': q.option_b,
                'C': q.option_c,
                'D': q.option_d
            },
            "category": q.category
        } for q in questions])


class SubmitAnswers(Resource):
    def post(self):
        data = request.get_json()
        user_name = data.get('user_name')
        answers = data.get('answers')  # e.g., [{"id": 1, "answer": "A"}, {"id": 2, "answer": "C"}]
        category = data.get('category')  # e.g., "Math", "Science", etc.

        if not user_name or not answers or not category:
            return {"message": "Missing required fields"}, 400

        total_points = 0

        for item in answers:
            question_id = item.get("id")
            user_answer = item.get("answer")

            question = Question.query.get(question_id)
            if not question:
                return {"message": f"Question with id {question_id} not found"}, 404

            correct_answers = set(question.correct_answers.split(','))
            if user_answer in correct_answers:
                total_points += question.points

        # Save result to the database with category
        result = Result.save_result(user_name, ','.join([f"{item['id']}:{item['answer']}" for item in answers]),
                                    total_points, category)

        return {"message": "Answers submitted successfully", "score": total_points}, 200


class LeaderboardAPI(Resource):
    def get(self):
        category = request.args.get('category')
        timeframe = request.args.get('timeframe')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        query = Leaderboard.query

        if category:
            query = query.filter_by(category=category)
        if timeframe:
            if timeframe == 'daily':
                start_time = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
                query = query.filter(Leaderboard.timestamp >= start_time)
            elif timeframe == 'weekly':
                start_time = datetime.utcnow() - timedelta(days=7)
                query = query.filter(Leaderboard.timestamp >= start_time)

        paginated_results = paginate_query(query.order_by(Leaderboard.score.desc()), page, per_page)

        return jsonify({
            'total': paginated_results.total,
            'page': paginated_results.page,
            'per_page': paginated_results.per_page,
            'results': [
                {
                    'user_id': record.user_id,
                    'category': record.category,
                    'score': record.score,
                    'timestamp': record.timestamp
                } for record in paginated_results.items
            ]
        })

class QuizHistoryAPI(Resource):
    def get(self):
        user_id = request.args.get('user_id', type=int)
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        if not user_id:
            return {'message': 'User ID is required'}, 400

        query = QuizHistory.query.filter_by(user_id=user_id)
        paginated_results = paginate_query(query.order_by(QuizHistory.timestamp.desc()), page, per_page)

        return jsonify({
            'total': paginated_results.total,
            'page': paginated_results.page,
            'per_page': paginated_results.per_page,
            'results': [
                {
                    'category': record.category,
                    'score': record.score,
                    'answers': record.answers,
                    'timestamp': record.timestamp
                } for record in paginated_results.items
            ]
        })

class CategoriesAPI(Resource):
    def get(self):
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        query = Category.query

        paginated_results = paginate_query(query, page, per_page)

        return jsonify({
            'total': paginated_results.total,
            'page': paginated_results.page,
            'per_page': paginated_results.per_page,
            'results': [
                {
                    'id': category.id,
                    'name': category.name,
                    'description': category.description
                } for category in paginated_results.items
            ]
        })

    def post(self):
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')

        if not name:
            return {'message': 'Category name is required'}, 400

        category = Category(name=name, description=description)
        try:
            db.session.add(category)
            db.session.commit()
            return {'message': 'Category created successfully'}, 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'message': 'Error creating category', 'error': str(e)}, 500

    def put(self):
        data = request.get_json()
        category_id = data.get('id')
        name = data.get('name')
        description = data.get('description')

        if not category_id or not name:
            return {'message': 'Category ID and name are required'}, 400

        category = Category.query.get(category_id)
        if not category:
            return {'message': 'Category not found'}, 404

        category.name = name
        category.description = description
        try:
            db.session.commit()
            return {'message': 'Category updated successfully'}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'message': 'Error updating category', 'error': str(e)}, 500

    def delete(self):
        category_id = request.args.get('id', type=int)

        if not category_id:
            return {'message': 'Category ID is required'}, 400

        category = Category.query.get(category_id)
        if not category:
            return {'message': 'Category not found'}, 404

        try:
            db.session.delete(category)
            db.session.commit()
            return {'message': 'Category deleted successfully'}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'message': 'Error deleting category', 'error': str(e)}, 500
