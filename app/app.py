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
    get_top_rated_movies_list,
    get_movie_list_specific_provider,
    get_genres
)

main = Blueprint("main", __name__)

# TODO: Find way to not use global variables
top_rated_movie_page = 1
provider = 'Any'

@main.route('/', methods=['POST', 'GET'])
def index():

    global provider
    global top_rated_movie_page

    if request.method == 'GET':
        top_rated_movie_page = 1

    top_rated_list = get_top_rated_movies_list(top_rated_movie_page)

    if request.method == 'POST':
        if 'Next' in request.form:
            top_rated_movie_page += 1
            top_rated_list = get_top_rated_movies_list(top_rated_movie_page)

            if provider != 'Any':
                top_rated_list = get_movie_list_specific_provider(top_rated_list, provider)

        elif 'Previous' in request.form:
            top_rated_movie_page = top_rated_movie_page - 1
            top_rated_list = get_top_rated_movies_list(top_rated_movie_page)
            
            if provider != 'Any':
                top_rated_list = get_movie_list_specific_provider(top_rated_list, provider)

        elif 'Filter' in request.form:
            provider = request.form['Provider']

            if provider == 'Any':
                top_rated_list = get_top_rated_movies_list(top_rated_movie_page)
            else:
                top_rated_list = get_movie_list_specific_provider(top_rated_list, provider)
        

    return render_template('index.html', top_rated_list=top_rated_list, page_number=top_rated_movie_page, provider=provider)


@main.route('/movie/<int:movie_id>', methods=['POST', 'GET'])
def movie_id(movie_id):
    
    provider_list = get_movie_provider_list(movie_id)
    movie_data = get_movie_from_id(movie_id)

    return render_template('movie.html', provider_list=provider_list, movie_data=movie_data)


@main.route('/roulette')
def roulettte():
    return 'placeholder for roulette'


# TODO: Find way to not use global variables
movie_list = []

@main.route('/search', methods=['POST', 'GET'])
def search():

    global provider
    result = request.args.get('q')
    movie_list = get_movie_search_list(result)

    if 'Filter' in request.form:
        provider = request.form['Provider']
        if provider != 'Any':
            movie_list = get_movie_list_specific_provider(movie_list, provider)
        else:
            movie_list = get_movie_search_list(result)

    elif provider != 'Any':
        movie_list = get_movie_list_specific_provider(movie_list, provider)

    return render_template('search.html', movie_list=movie_list, keyword=result, provider=provider)
    
    if request.method == 'GET':
        return redirect('/')

