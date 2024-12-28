from flask_cors import cross_origin
from flask_restful import Resource
from flask import request, jsonify

from db.setup_db import db
from models.question_model import Question
from flask_jwt_extended import jwt_required

class QuestionCreate(Resource):
    @jwt_required()  # Ensure the user is authenticated
    def post(self):
        data = request.get_json()
        question_text = data.get('question')
        options = {
            'A': data.get('option_a'),
            'B': data.get('option_b'),
            'C': data.get('option_c'),
            'D': data.get('option_d')
        }
        correct_answers = data.get('correct_answers')  # e.g., "A,C"
        points = data.get('points')
        category = data.get('category')

        # Validate data
        if not question_text or not correct_answers or not points or not category:
            return {"message": "Missing required fields"}, 400

        question = Question(
            question=question_text,
            option_a=options['A'],
            option_b=options['B'],
            option_c=options['C'],
            option_d=options['D'],
            correct_answers=correct_answers,
            points=points,
            category=category
        )
        db.session.add(question)
        db.session.commit()

        return {"message": "Question created successfully"}, 201

class QuestionEdit(Resource):
    @jwt_required()  # Ensure the user is authenticated
    def put(self, question_id):
        data = request.get_json()
        updated_question = Question.edit_question(question_id, data)
        if not updated_question:
            return {"message": "Question not found or failed to update"}, 404
        return {"message": "Question updated successfully"}, 200

class QuestionDelete(Resource):
    @jwt_required()  # Ensure the user is authenticated
    def delete(self, question_id):
        deleted = Question.delete_question(question_id)
        if not deleted:
            return {"message": "Question not found or failed to delete"}, 404
        return {"message": "Question deleted successfully"}, 200

class QuestionDeletePremenent(Resource):
    @jwt_required()
    def delete(self,question_id):
        deleted = Question.delete_question_permenently(question_id)
        if not deleted:
            return {"message": "Question not found or failed to delete"}, 404
        return {"message": "Question deleted successfully"}, 200


class QuestionsByCategory(Resource):
    @jwt_required()
    @cross_origin(origins="http://localhost:3000")
    def get(self,category):
        questions = Question.get_questions_by_category(category)
        if questions:
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
        return {"Message" : f"No Question Found by Category {category}" }

class Categories(Resource):
    @jwt_required()
    def get(self):
        categories = Question.get_all_categories()
        if categories:
            return jsonify({"categories": categories})
        return jsonify({"message": "No categories found"})


class GetQuestion(Resource):
    @jwt_required()
    def get(self, question_id):
        try:
            # Attempt to fetch the question from the database
            question = Question.get_question_by_id(question_id)

            if question:
                # Return question data as JSON
                return jsonify({
                    'id': question.id,
                    'question': question.question,
                    'option_a': question.option_a,
                    'option_b': question.option_b,
                    'option_c': question.option_c,
                    'option_d': question.option_d,
                    'correct_answers': question.correct_answers,
                    'points': question.points,
                    'category': question.category,
                    'is_deleted': question.is_deleted,
                    'is_updated': question.is_updated
                })
            else:
                # If no question is found, return a 404 response with an appropriate message
                return jsonify({'message': 'Question not found'}), 404
        except Exception as e:
            # Handle any unexpected errors
            return jsonify({'message': 'An error occurred', 'error': str(e)}), 500