"""CRUD Operations."""

from model import db, User, Movie, Rating, connect_to_db

# creates and returns a new user
def create_user(email, password):


    user = User(email=email, password=password)

    return user

def get_movies():
    # Returns all Movie objects in a list
    return Movie.query.all()

def get_movie_by_id(movie_id):
    # Grabs movie by it's id

    return Movie.query.get(movie_id)

def get_users():
    return User.query.all()

def get_user_by_email(email):
    return User.query.filter(User.email == email).first()

# creates and returns a new movie
def create_movie(title, overview, release_date, poster_path):

    movie = Movie(title=title, 
                  overview=overview, 
                  release_date=release_date, 
                  poster_path=poster_path)

    return movie

# creates and returns a new rating
def create_rating(user_id, movie_id, score):

    rating = Rating(user_id=user_id, movie_id=movie_id, score=score)

    return rating

if __name__ == '__main__':
    from server import app
    connect_to_db(app)