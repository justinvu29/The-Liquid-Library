from model import db, User, FavoriteCocktail, connect_to_db

def create_user(email, password):
    user = User(email=email, password=password)
    return user

def create_cocktail(user_id, cocktail_id):
    cocktail = FavoriteCocktail(user_id=user_id, cocktail_id=cocktail_id)
    return cocktail

if __name__ == '__main__':
    from server import app
    connect_to_db(app)