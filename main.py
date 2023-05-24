from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import requests
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'top_secret'
Bootstrap(app)

headers = {
    'Accept': 'application/json',
    'Authorization': 'GET YOUR API_KEY FROM: https://the-one-api.dev/'
}
url = 'https://the-one-api.dev/v2'
book_url = 'https://the-one-api.dev/v2/book/'

############### This is to save the data from the API in a local database as to not make a lot of requests ############
############### Because I only used this for testing purposes I have not yet implemented this functionality ###########

# db = SQLAlchemy()
#app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies.db"
# db.init_app(app)

# class Movie(db.Model):
#     __tablename = 'movie'
#     id = db.Column(db.Integer, primary_key=True)
#     _id = db.Column(db.String, unique=True)
#     name = db.Column(db.String)
#     runtimeInMinutes = db.Column(db.Integer)
#     budgetInMillions = db.Column(db.Integer)
#     boxOfficeRevenueInMillions = db.Column(db.Integer)
#     academyAwardNominations = db.Column(db.Integer)
#     academyAwardWins = db.Column(db.Integer)
#     rottenTomatoesScore = db.Column(db.Float)
#
#
# class Characters(db.Model):
#     __tablename__ = 'characters'
#     id = db.Column(db.Integer, primary_key=True)
#     _id = db.Column(db.String, unique=True)
#     height = db.Column(db.String)
#     race = db.Column(db.String)
#     gender = db.Column(db.String)
#     birth = db.Column(db.String)
#     spouse = db.Column(db.String)
#     death = db.Column(db.String)
#     realm = db.Column(db.String)
#     hair = db.Column(db.String)
#     name = db.Column(db.String)
#     wikiUrl = db.Column(db.String)
#
#
# class Quotes(db.Model):
#     __tablename = 'quotes'
#     id = db.Column(db.Integer, primary_key=True)
#     _id = db.Column(db.String, unique=True)
#     dialog = db.Column(db.String)
#     movie = db.Column(db.String)
#     character = db.Column(db.String)
#     id_ = db.Column(db.String)


@app.route('/', methods=["GET", "POST"])
def home():
    all_quotes = requests.get(url + '/quote', headers=headers).json()
    choice = random.choice(all_quotes['docs'])
    name = requests.get(url + f"/character/{choice['character']}", headers=headers).json()
    return render_template('index.html', choice=choice, name=name['docs'])


@app.route('/books', methods=["GET", "POST"])
def books():
    all_books = requests.get(url + '/book').json()
    book_id = [doc['_id'] for doc in all_books['docs']]
    book_name = all_books['docs']
    book1_chapters = requests.get(book_url +book_id[0] +'/chapter').json()['docs']
    book2_chapters = requests.get(book_url +book_id[1] +'/chapter').json()['docs']
    book3_chapters = requests.get(book_url +book_id[2] +'/chapter').json()['docs']
    return render_template('books.html', book_id=book_id, book_name=book_name, book1_chapters=book1_chapters, book2_chapters=book2_chapters, book3_chapters=book3_chapters)


@app.route('/movies', methods=["GET", "POST"])
def movies():
    all_movies = requests.get(url + '/movie', headers=headers).json()
    return render_template('movies.html', all_movies=all_movies['docs'])


@app.route('/character', methods=["GET", "POST"])
def character():
    all_characters = requests.get(url + '/character', headers=headers).json()
    choice = random.choice(all_characters['docs'])
    return render_template('character.html', choice=choice)


@app.route('/characters', methods=["GET", "POST"])
def characters():
    all_characters = requests.get(url + '/character', headers=headers).json()
    return render_template('characters.html', all_characters=all_characters['docs'])


@app.route('/quote', methods=["GET", "POST"])
def quote():
    all_quotes = requests.get(url + '/quote', headers=headers).json()
    choice = random.choice(all_quotes['docs'])
    name = requests.get(url + f"/character/{choice['character']}", headers=headers).json()
    movie = requests.get(url + f"/movie/{choice['movie']}", headers=headers).json()
    return render_template('quote.html', choice=choice, name=name['docs'], movie=movie['docs'])


if __name__ == '__main__':
    app.run(debug=True)