from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, TextAreaField
from wtforms.validators import DataRequired, NumberRange
import os


app = Flask(__name__)
# creates instance folder, if it's not present already:
instance_path = os.path.join(os.getcwd(), 'instance')
if not os.path.exists(instance_path):
    os.makedirs(instance_path)
db_path = os.path.join(instance_path, 'new-movies-collection.db')
print(f'Database will be created at: {db_path}')
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # disables tracking modifications
Bootstrap5(app)
db = SQLAlchemy(app)

# CREATE DB
# Defines the Movie model (modern approach, with Type Checking)
class Movie(db.Model):
    __tablename__ = 'movies'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), nullable=False, unique=True)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)
    ranking: Mapped[int] = mapped_column(Integer, nullable=False)
    review: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)


with app.app_context():
    db.create_all()

    # adds a new movie:
    if not Movie.query.filter_by(id=1).first():
        new_movie = Movie(
            title="Phone Booth",
            year=2002,
            description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
            rating=7.3,
            ranking=10,
            review="My favorite character was the caller.",
            img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
        )
        db.session.add(new_movie)
        db.session.commit()

    if not Movie.query.filter_by(id=2).first():
        second_movie = Movie(
            title="Avatar The Way of Water",
            year=2022,
            description="Set more than a decade after the events of the first film, learn the story of the Sully family (Jake, Neytiri, and their kids), the trouble that follows them, the lengths they go to keep each other safe, the battles they fight to stay alive, and the tragedies they endure.",
            rating=7.3,
            ranking=9,
            review="I liked the water.",
            img_url="https://image.tmdb.org/t/p/w500/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg"
        )
        db.session.add(second_movie)
        db.session.commit()

# CREATE TABLE

class RateMovieForm(FlaskForm):
    rating = FloatField("Your Rating Out of 10: (you can include a decimal)", validators=[DataRequired(), NumberRange(min=0, max=10)])
    review = TextAreaField("Your Review:", validators=[DataRequired()])
    submit = SubmitField("Done")


@app.route("/")
def home():
    movies = Movie.query.all()
    return render_template("index.html", movies=movies)


@app.route('/edit_form/<int:movie_id>', methods=['GET', 'POST'])
def edit_form(movie_id):
    movie = Movie.query.get(movie_id)
    if not movie:
        return "Movie not found", 404
    form = RateMovieForm(obj=movie)
    if form.validate_on_submit():
        movie.rating = form.rating.data
        movie.review = form.review.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit.html', movie=movie, form=form)


@app.route('/delete/<int:movie_id>', methods=['POST'])
def delete_movie(movie_id):
    movie_to_delete = Movie.query.get(movie_id)
    if movie_to_delete:
        db.session.delete(movie_to_delete)
        db.session.commit()
        return redirect(url_for('home'))
    else:
        return "This movie was not found", 404


if __name__ == '__main__':
    app.run(debug=True)
