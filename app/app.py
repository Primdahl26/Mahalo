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
    get_movie_list_specific_provider
)

main = Blueprint("main", __name__)

top_rated_movie_page = 1

@main.route('/', methods=['POST', 'GET'])
def index():

    provider = 'Any'
    global top_rated_movie_page
    top_rated_list = get_top_rated_movies_list(top_rated_movie_page)
    
    if request.method == 'GET':
        top_rated_movie_page = 1
        

    if request.method == 'POST':
        if 'Next' in request.form:
            top_rated_movie_page += 1
            top_rated_list = get_top_rated_movies_list(top_rated_movie_page)

        elif 'Filter' in request.form:
            if request.form.get('Provider') == 'Netflix':
                provider = 'Netflix'
                top_rated_list = get_movie_list_specific_provider(top_rated_list, 'Netflix')

            elif request.form.get('Provider') == 'HBO':
                provider = 'HBO'
                top_rated_list = get_movie_list_specific_provider(top_rated_list, 'HBO')

            elif request.form.get('Provider') == 'Any':
                provider = 'Any'
                top_rated_list = get_top_rated_movies_list(top_rated_movie_page)

    return render_template('index.html', top_rated_list=top_rated_list, page_number=top_rated_movie_page, provider=provider)


@main.route('/movie/<int:movie_id>', methods=['POST', 'GET'])
def movie_id(movie_id):
    
    provider_list = get_movie_provider_list(movie_id)
    movie_data = get_movie_from_id(movie_id)

    return render_template('movie.html', provider_list=provider_list, movie_data=movie_data)


@main.route('/roulette')
def roulettte():
    return 'placeholder for roulette'

# TODO: Fix so this can filter through the movie list too
# i get 400 bad request when i try to filter a movie in the search
# i think it might be because flask cannot find Filter in request.form
@main.route('/search', methods=['POST', 'GET'])
def search():
    
    result = request.form['search_text']
    movie_list = get_movie_search_list(result)

    if request.method == 'POST':
        if 'Filter' in request.form:
            if request.form.get('Provider') == 'Netflix':
                provider = 'Netflix'
                movie_list = get_movie_list_specific_provider(movie_list, 'Netflix')

            elif request.form.get('Provider') == 'HBO':
                provider = 'HBO'
                movie_list = get_movie_list_specific_provider(movie_list, 'HBO')

            elif request.form.get('Provider') == 'Any':
                result = request.form['search_text']
                provider = 'Any'
                movie_list = get_movie_search_list(result)
                
        return render_template('search.html', movie_list=movie_list, keyword=result)
    
    else:
        return render_template('index.html')

