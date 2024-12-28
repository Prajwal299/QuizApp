from db.setup_db import db

from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # Ensure enough length to store hashed passwords
    is_admin = db.Column(db.Boolean, default=False)

    @staticmethod
    def find_by_email(email):
        res = User.query.filter_by(email=email).first()
        if res:
            return res


    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
