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
    get_movie_list_specific_provider,
    get_genres,
    get_movie_list
)

main = Blueprint("main", __name__)

# TODO: Find way to not use global variables
provider = 'Any'

@main.route('/', methods=['POST', 'GET'])
def index():

    global provider
    page = 1 

    if request.method == 'GET':
        provider = 'Any'
        page = 1

    top_rated_list = get_movie_list(page, 'top_rated')
    top_rated_list.extend(get_movie_list(page+1, 'top_rated'))
    print('Top rated list size:')
    print(len(top_rated_list))

    popular_list = get_movie_list(page, 'popular')
    popular_list.extend(get_movie_list(page+1, 'popular'))
    print('Popular list size:')
    print(len(popular_list))

    upcoming_list = get_movie_list(page, 'upcoming')
    upcoming_list.extend(get_movie_list(page+1, 'upcoming'))
    print('Upcoming list size:')
    print(len(upcoming_list))


    if request.method == 'POST':
        if 'Filter' in request.form:
            provider = request.form['Provider']

            if provider == 'Any':
                top_rated_list = get_movie_list(page, 'top_rated')
                top_rated_list.extend(get_movie_list(page+1, 'top_rated'))

                popular_list = get_movie_list(page, 'popular')
                popular_list.extend(get_movie_list(page+1, 'popular'))

                upcoming_list = get_movie_list(page, 'upcoming')
                upcoming_list.extend(get_movie_list(page+1, 'upcoming'))

            else:
                top_rated_list = get_movie_list_specific_provider(top_rated_list, provider)
                popular_list = get_movie_list_specific_provider(popular_list, provider)
                upcoming_list = get_movie_list_specific_provider(upcoming_list, provider)
        

    return render_template('main.html', top_rated_movies=top_rated_list, popular_movies=popular_list, upcoming_movies=upcoming_list)


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

    return render_template('search2.html', movie_list=movie_list, keyword=result, provider=provider)
    
    if request.method == 'GET':
        return redirect('/')

