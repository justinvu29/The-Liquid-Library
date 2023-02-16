"""Server for liquid library app."""
from flask import Flask, render_template, request
import jinja2
import requests
import random
from model import connect_to_db, db, Cocktail, Favorite


app = Flask(__name__)


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

@app.route('/add_to_favorites', methods=['POST'])
def add_to_favorites():
    cocktail_id = request.form['cocktail_id']
    user_id = request.form['user_id']
    favorite = Favorite(cocktail_id=cocktail_id, user_id=user_id)
    db.session.add(favorite)
    db.session.commit()
    return 'Added to favorites!'

@app.route('/favorites')
def favorites():
    user_id = request.args.get('user_id')
    favorites = Favorite.query.filter_by(user_id=user_id).all()
    cocktail_ids = [favorite.cocktail_id for favorite in favorites]
    cocktails = Cocktail.query.filter(Cocktail.id.in_(cocktail_ids)).all()
    return render_template('favorites.html', cocktails=cocktails)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
