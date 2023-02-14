"""Server for liquid library app."""
from flask import Flask, render_template, request
import jinja2
import requests

app = Flask(__name__)


@app.route('/')
def homepage():
    if 'GO' in request.args:
        name = request.args.get('search').strip()
        url = f'https://www.thecocktaildb.com/api/json/v1/1/search.php?s={name}'
        res = requests.get(url)
        res = res.json()
        cocktail = res['drinks'][0]
        return render_template('home.html', cocktail = cocktail)
    else:
        return render_template('search.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
