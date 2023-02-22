import os
from random import choice, randint

from model import User, db, FavoriteCocktail

import crud
import model
import server

with server.app.app_context():

    os.system("dropdb library")
    os.system("createdb library")

    model.connect_to_db(server.app)
    model.db.create_all()
    model.db.session.commit()

with server.app.app_context():

    alice = User("alice@example.com", "password123")
    bob = User("bob@example.com", "password123")
    db.session.add_all([alice, bob])
    db.session.commit()

with server.app.app_context():

    alice_favorites = [
        FavoriteCocktail(1, 11007),
        FavoriteCocktail(1, 11008),
        FavoriteCocktail(1, 11009)
    ]
    db.session.add_all(alice_favorites)
    db.session.commit()

    bob_favorites = [
        FavoriteCocktail(2, 11011),
        FavoriteCocktail(2, 11012),
        FavoriteCocktail(2, 11013)
    ]
    db.session.add_all(bob_favorites)
    db.session.commit()