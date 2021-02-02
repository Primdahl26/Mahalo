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

from .api import get_movie_dict, get_movie_providers

main = Blueprint("main", __name__)

@main.route('/')
def index():
    return render_template('index.html')

# TODO: Fix so that this returns movie information from a movie ID
@main.route('/movie/<int:movie_id>')
def movie_id(movie_id):

    movie_provider_dict = get_movie_providers(movie_id)

    return render_template('movie.html', movie_providers=movie_provider_dict)

@main.route('/roulette')
def roulettte():
    return 'placeholder for roulette'

@main.route('/search', methods=['POST', 'GET'])
def search():

    if request.method == 'POST':
        
        result = request.form['searchText']

        movie_dict = get_movie_dict(result)

        return render_template('search.html', movie_dict=movie_dict)