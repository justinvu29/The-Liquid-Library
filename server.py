"""Server for liquid library app."""
from flask import (Flask, render_template, request, flash, session, url_for, redirect)
from datetime import timedelta
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from forms import LoginForm, RegisterForm
import jinja2
import requests
import random
from model import connect_to_db, db, User, FavoriteCocktail


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)

app.config['SECRET_KEY'] = 'secret-key'
app.config['LOGIN_VIEW'] = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

"""Login Function """
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    register_form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        remember_me = form.remember_me.data

        print(email)
        print(password)
        print(remember_me)

        user = User.query.filter_by(email=email).first()

        if user:
            if user.password == password:
                login_user(user, remember=remember_me, duration=timedelta(days=7))
                return redirect(url_for("homepage"))
            return "Your username or password does not match our records."  
        else:
            return render_template("login.html", form=form, register_form=register_form)
    return render_template("login.html", form=form, register_form=register_form)

@app.route("/register", methods=["POST"])
def register():
    form = RegisterForm()

    email = form.email.data
    password = form.password.data
    confirm_password = form.confirm_password.data

    print(email)
    print(password)
    print(confirm_password)

    user = User.query.filter_by(email=email).first()

    if user:
        return "Username already exists."
    if password != confirm_password:
        return "Passwords do not match."
    
    new_user = User(email, password)
    db.session.add(new_user)
    db.session.commit()

    return "hey"


"""Logout Function"""
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route('/')
def homepage():
    if 'GO' in request.args:
        name = request.args.get('search').strip()
        url = f'https://www.thecocktaildb.com/api/json/v1/1/search.php?s={name}'
        res = requests.get(url)
        res = res.json()
        cocktail = res['drinks'][0]
        return render_template('home.html', cocktail=cocktail)
    elif 'Random' in request.args:
        url = 'https://www.thecocktaildb.com/api/json/v1/1/random.php'
        res = requests.get(url)
        res = res.json()
        cocktail = res['drinks'][0]
        return render_template('home.html', cocktail=cocktail)
    else:
        return render_template('search.html')


@app.route('/favorites')
def favorites():
    return "Favorites Page"


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
