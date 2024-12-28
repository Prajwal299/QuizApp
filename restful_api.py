from flask import Blueprint
from flask_restful import Api

from controllers.question_controller import QuestionCreate, QuestionEdit, QuestionDelete, \
    QuestionDeletePremenent, QuestionsByCategory, Categories, GetQuestion
from controllers.token_refresh_controller import TokenRefresh
from controllers.user_controller import UserRegistration, UserLogin, AdminResults, UserResult
from controllers.view_results import QuestionList, SubmitAnswers, LeaderboardAPI, QuizHistoryAPI, CategoriesAPI

restful_api_bp = Blueprint('restful_api', __name__)
api = Api(restful_api_bp)

# Routes
api.add_resource(UserRegistration, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(TokenRefresh, '/refresh')

# Admin quiz routes
api.add_resource(QuestionCreate, '/admin/create_question')
api.add_resource(QuestionEdit, '/admin/edit_question/<int:question_id>')
api.add_resource(QuestionDelete, '/admin/delete_question/<int:question_id>')
api.add_resource(QuestionDeletePremenent, '/admin/delete_question/<int:question_id>')
api.add_resource(QuestionsByCategory,'/admin/get_questions/<string:category>')
#api.add_resource(Categories, '/admin/categories')
api.add_resource(GetQuestion,"/admin/get_question/<int:question_id>")

# User quiz routes
api.add_resource(QuestionList, '/questions/<string:category>')
api.add_resource(Categories, '/categories')
api.add_resource(SubmitAnswers, '/submit_answers')
api.add_resource(LeaderboardAPI, '/leaderboard')
api.add_resource(QuizHistoryAPI, '/user/history')


api.add_resource(AdminResults, '/admin/results')
api.add_resource(UserResult, '/user/results/<string:user_name>')
