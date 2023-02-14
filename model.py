from flask_sqlalchemy import SQLAlchemy
import os


db = SQLAlchemy()

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    favorites = db.relationship('Favorite', backref='user', lazy=True)

    def __repr__(self):
        return f"<User user_id={self.user_id} email={self.email}>"

class Cocktail(db.Model):

    __tablename__ = "cocktails"

    id = db.Column(db.Integer, primary_key=True)
    cocktail_name = db.Column(db.String(120), nullable=False)
    instructions = db.Column(db.String(500), nullable=False)
    alcoholic = db.Column(db.Boolean, nullable=False)
    image_url = db.Column(db.String(500), nullable=False)
    ingredients = db.relationship('Ingredient', backref='cocktail', lazy=True)


    def __repr__(self):
        return f"<Cocktail cocktail_id={self.cocktail_id} cocktail_name={self.cocktail_name}>"


class Ingredient(db.Model):

    __tablename__ = "ingredients"

    id = db.Column(db.Integer, primary_key=True)
    ingredient_name = db.Column(db.String(120), nullable=False)
    measurement = db.Column(db.String(120), nullable=False)
    cocktail_id = db.Column(db.Integer, db.ForeignKey('cocktail.id'), nullable=False)

    def __repr__(self):
        return f"<Ingredient ingredient_id={ingredient_id} ingredient_name={ingredient_name}>"


class Favorite(db.Model):

    __tablename__ = "favorites"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    cocktail_id = db.Column(db.Integer, db.ForeignKey('cocktail.id'), nullable=False)


    def __repr__(self):
        return f"<Favorite cocktail_id={self.cocktail_id} user_id={self.user_id}>"


def connect_to_db(flask_app, db_uri = os.environ["POSTGRES_URI"], echo=False):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app
    connect_to_db(app)