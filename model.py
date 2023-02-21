from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import os


db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __repr__(self):
        return f"<User id={self.id}, email={self.email}>"


class FavoriteCocktail(db.Model):
    __tablename__ = "favorite_cocktails"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    cocktail_id = db.Column(db.Integer, nullable=False)

    def __init__(self, user_id, cocktail_id):
        self.user_id = user_id
        self.cocktail_id = cocktail_id

    def __repr__(self):
        return f"<FavoriteCocktail id={self.id}, user_id={self.user_id}, cocktail_id={self.cocktail_id}>"



def connect_to_db(flask_app, db_uri = os.environ["POSTGRES_URI"], echo=False):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to Database...")


if __name__ == "__main__":
    from server import app
    connect_to_db(app)