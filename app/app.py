import json
from flask import (
    Blueprint,
    current_app,
    flash,
    g,
    redirect,
    render_template,
    request,
    url_for,
    make_response,
)

from .api import get_movies, get_movie_providers

main = Blueprint("main", __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/roulette')
def roulettte():
    return 'placeholder for roulette'

@main.route('/search')
def search():

    get_movies('Wonder woman')

    return 'Hello'