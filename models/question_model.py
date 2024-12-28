from db.setup_db import db

class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(255), nullable=False)
    option_a = db.Column(db.String(255), nullable=False)
    option_b = db.Column(db.String(255), nullable=False)
    option_c = db.Column(db.String(255), nullable=False)
    option_d = db.Column(db.String(255), nullable=False)
    correct_answers = db.Column(db.String(255), nullable=False)  # store comma separated correct options (e.g., "A,C")
    points = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    is_deleted = db.Column(db.Boolean, default=False)
    is_updated = db.Column(db.Boolean, default=False)

    @staticmethod
    def get_all_by_category(category):
        return Question.query.filter_by(category=category, is_deleted=False).all()

    @staticmethod
    def edit_question(id, question_data):
        question = Question.query.get(id)
        if question:
            question.question = question_data.get('question', question.question)
            question.option_a = question_data.get('option_a', question.option_a)
            question.option_b = question_data.get('option_b', question.option_b)
            question.option_c = question_data.get('option_c', question.option_c)
            question.option_d = question_data.get('option_d', question.option_d)
            question.correct_answers = question_data.get('correct_answers', question.correct_answers)
            question.points = question_data.get('points', question.points)
            question.category = question_data.get('category', question.category)
            question.is_updated = True
            db.session.commit()
            return question
        return None

    @staticmethod
    def delete_question(id):
        question = Question.query.get(id)
        if question:
            question.is_deleted = True
            db.session.commit()
            return True
        return False

    @staticmethod
    def delete_question_permenently(id):
        question = Question.query.get(id)
        if question:
            db.session.delete(question)
            db.session.commit()
            return True
        return False

    @staticmethod
    def get_questions_by_category(category):
        questions = Question.query.filter_by(category=category).all()
        if questions:
            return questions
        return None

    @staticmethod
    def get_all_categories():
        # Fetch unique categories
        categories = db.session.query(Question.category).filter(Question.is_deleted == 0).distinct().all()
        return [category[0] for category in categories]

    @staticmethod
    def get_question_by_id(id):
        # Fetch the question by its ID, ensuring it's not deleted
        ques = Question.query.filter_by(id=id, is_deleted=0).first()
        if ques:
            return ques
        return None

