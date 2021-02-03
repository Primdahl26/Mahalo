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

from .api import (
    get_movie_search_list, 
    get_movie_provider_list, 
    get_movie_from_id, 
    get_top_rated_movies_list
)

main = Blueprint("main", __name__)

top_rated_movie_page = 0

@main.route('/', methods=['POST', 'GET'])
def index():

    global top_rated_movie_page
    
    if request.method == 'GET':
        top_rated_movie_page = 1
        top_rated_list = get_top_rated_movies_list(top_rated_movie_page)

    if request.method == 'POST':
        if request.form.get('Next') == 'Next':
            top_rated_movie_page += 1
            top_rated_list = get_top_rated_movies_list(top_rated_movie_page)

    return render_template('index.html', top_rated_list=top_rated_list)


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
        movie_list = get_movie_search_list(result)

        return render_template('search.html', movie_list=movie_list)
    
    else:
        return render_template('index.html')

