"""Server for movie ratings app."""

from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/movies')
def all_movies():

    # Returns all movies from Movie obj
    movies = crud.get_movies()

    return render_template("all_movies.html", movies=movies)

@app.route("/movies/<movie_id>")
def show_movie(movie_id):
    # Details for the user after clicking on the desired movie

    movie = crud.get_movie_by_id(movie_id)

    return render_template("movie_details.html", movie=movie)

@app.route('/users')
def all_users():
    
    users = crud.get_users()

    return render_template("all_users.html", users=users)


@app.route('/users', methods=["POST"])
def new_user():
    "Creates a new user"

    new_email = request.form.get("email")
    new_pass = request.form.get("password")

    user = crud.get_user_by_email(new_email)

    if (user):
        flash("An account with this email already exists!")
    else:
        new_user = crud.create_user(new_email, new_pass)
        # no need for app.app_context() since this is in a view function
        db.session.add(new_user)
        db.session.commit()
        flash("Account created!")
            
    return redirect("/")

@app.route('/login', methods=["POST"])
def login():
    """Allows users to log in using their provided credentials"""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)

    if not user or user.password != password:
        flash("Username or Password is incorrect")
    else:
        # Stores user email in a session obj on server side
        # session is a dictionary object that can set session variables, so below I created the "user_email" key value pair then set the session obj to user.email
        session["user_email"] = user.email
        flash(f"Welcome back, {user.email}!")

    return redirect("/")

@app.route("/movies/<movie_id>/ratings", methods=["POST"])
def create_rating(movie_id):
    """Creates new rating for specified movie"""

    score = request.form.get("rating")
    email = session.get("user_email")

    if email == None:
        flash("Please log in to rate this movie")
    elif not score:
        flash("Please select a rating score")
    else:
        user = crud.get_user_by_email(email)
        movie = crud.get_movie_by_id(movie_id)

        rating = crud.create_rating(user.user_id, movie.movie_id, int(score))
        db.session.add(rating)
        db.session.commit()

        flash(f"You rated this movie {score} out of 5.")

    return redirect(f"/movies/{movie_id}")

        
if __name__ == "__main__":

    connect_to_db(app)
    app.run(host="0.0.0.0", debug=False)