from decouple import config
import json
import requests

api_key = config('THE_MOVIE_DB_API_KEY')
language_url = '&language=dk'


def get_movie_search_list(keyword):
     
    search_api_url = f'https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={keyword}' + language_url
    data = requests.get(search_api_url).json()

    movie_list = []

    for element in data['results']:
        # If the poster image os none, and there is no release_date,
        # then we use Unknown as release_date, and a ? image for the poster
        if element['poster_path'] is None and 'release_date' not in element:
            temp_dict = {'id' : element['id'], 'title': element['title'], 'release_date': 'Unknown', 'poster_path': 'https://upload.wikimedia.org/wikipedia/commons/2/2f/QuestionMark.jpg'}
            movie_list.append(temp_dict)
        # If there is no release date,
        # then we use Unknown as release_date
        elif 'release_date' not in element:
            temp_dict = {'id' : element['id'], 'title': element['title'], 'release_date': 'Unknown', 'poster_path': 'https://image.tmdb.org/t/p/w500/' + element['poster_path']}
            movie_list.append(temp_dict)
        # If the poster image is none,
        # then we use a ? image for the poster
        elif element['poster_path'] is None:
            temp_dict = {'id' : element['id'], 'title': element['title'], 'release_date': element['release_date'], 'poster_path': 'https://upload.wikimedia.org/wikipedia/commons/2/2f/QuestionMark.jpg'}
            movie_list.append(temp_dict)
        # Else all the information we need is there
        else:
            temp_dict = {'id' : element['id'], 'title': element['title'], 'release_date': element['release_date'], 'poster_path': 'https://image.tmdb.org/t/p/w500/' + element['poster_path']}
            movie_list.append(temp_dict)

    return movie_list


# TODO: Make it support more than danish & more than flatrate
# Right now it only gets danish providers & it only gets flatrate options (streaming as netflix)
def get_movie_provider_list(movie_id):

    search_api_url = f'https://api.themoviedb.org/3/movie/{movie_id}/watch/providers?api_key={api_key}'+ language_url
    data = requests.get(search_api_url).json()

    provider_list = []

    if 'DK' in data['results']:
        if 'flatrate' in data['results']['DK']:
            for element in data['results']['DK']['flatrate']:
                temp_dict = {'id' : element['provider_id'], 'name': element['provider_name'], 'logo_path': 'https://image.tmdb.org/t/p/original' + element['logo_path']}
                provider_list.append(temp_dict)
        else:
            provider_list.append({'Providers' : 'None_DK'})
    else:
        provider_list.append({'Providers' : 'None_DK'})

    return provider_list


def get_movie_from_id(movie_id):

    search_api_url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}'+ language_url
    data = requests.get(search_api_url).json()

    movie_data = [{
        'id' : data['id'],
        'title' : data['title'],
        'release_date' : data['release_date'],
    }]

    if data['poster_path'] is not None:
        movie_data[0]['poster_path'] = 'https://image.tmdb.org/t/p/w500/' + data['poster_path']
    else:
        movie_data[0]['poster_path'] = 'https://upload.wikimedia.org/wikipedia/commons/2/2f/QuestionMark.jpg'

    return movie_data


def get_top_rated_movies_list(page):

    page_url = '&page=' + str(page)

    search_api_url = f'https://api.themoviedb.org/3/movie/top_rated?api_key={api_key}'+ language_url + page_url
    data = requests.get(search_api_url).json()

    top_rated_movie_list = []

    for element in data['results']:
        # If the poster image os none, and there is no release_date,
        # then we use Unknown as release_date, and a ? image for the poster
        if element['poster_path'] is None and 'release_date' not in element:
            temp_dict = {'id' : element['id'], 'title': element['title'], 'release_date': 'Unknown', 'poster_path': 'https://upload.wikimedia.org/wikipedia/commons/2/2f/QuestionMark.jpg'}
            top_rated_movie_list.append(temp_dict)
        # If there is no release date,
        # then we use Unknown as release_date
        elif 'release_date' not in element:
            temp_dict = {'id' : element['id'], 'title': element['title'], 'release_date': 'Unknown', 'poster_path': 'https://image.tmdb.org/t/p/w500/' + element['poster_path']}
            top_rated_movie_list.append(temp_dict)
        # If the poster image is none,
        # then we use a ? image for the poster
        elif element['poster_path'] is None:
            temp_dict = {'id' : element['id'], 'title': element['title'], 'release_date': element['release_date'], 'poster_path': 'https://upload.wikimedia.org/wikipedia/commons/2/2f/QuestionMark.jpg'}
            top_rated_movie_list.append(temp_dict)
        # Else all the information we need is there
        else:
            temp_dict = {'id' : element['id'], 'title': element['title'], 'release_date': element['release_date'], 'poster_path': 'https://image.tmdb.org/t/p/w500/' + element['poster_path']}
            top_rated_movie_list.append(temp_dict)

    return top_rated_movie_list

# Takes a list of movies, and returns only the movies that are streamable
# on the provider in the parameter
def get_movie_list_specific_provider(movie_list, provider):

    specific_movie_list = []
    
    if provider == 'Netflix':
        for element in movie_list:
            for item in get_movie_provider_list(element['id']):
                if 'name' in item:
                    if item['name'] == 'Netflix':
                        specific_movie_list.append(element)

    elif provider == 'HBO':
        for element in movie_list:
            for item in get_movie_provider_list(element['id']):
                if 'name' in item:
                    if item['name'] == 'HBO':
                        specific_movie_list.append(element)

    return specific_movie_list