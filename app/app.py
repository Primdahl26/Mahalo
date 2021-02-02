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

from .api import get_movie_list, get_movie_provider_list, get_movie_from_id

main = Blueprint("main", __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/movie/<int:movie_id>', methods=['POST', 'GET'])
def movie_id(movie_id):
    
    provider_list = get_movie_provider_list(movie_id)
    movie_data = get_movie_from_id(movie_id)

    return render_template('movie.html', provider_list=provider_list, movie_data=movie_data)


@main.route('/roulette')
def roulettte():
    return 'placeholder for roulette'


@main.route('/search', methods=['POST', 'GET'])
def search():

    if request.method == 'POST':
        result = request.form['searchText']
        movie_list = get_movie_list(result)

        return render_template('search.html', movie_list=movie_list)
    
    else:
        return render_template('index.html')