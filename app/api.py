from decouple import config
import json
import requests

api_key = config('THE_MOVIE_DB_API_KEY')
language_url = '&language=dk'


def get_movie_list(keyword):
    search_api_url = f'https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={keyword}' + language_url
    data = requests.get(search_api_url).json()

    movie_list = []

    for element in data['results']:
        if element['poster_path'] is None and 'release_date' not in data['results']:
            temp_dict = {'id' : element['id'], 'title': element['title'], 'release_date': 'Unknown', 'poster_path': 'https://upload.wikimedia.org/wikipedia/commons/2/2f/QuestionMark.jpg'}
            movie_list.append(temp_dict)
        elif 'release_date' not in data['results']:
            temp_dict = {'id' : element['id'], 'title': element['title'], 'release_date': 'Unknown', 'poster_path': 'https://image.tmdb.org/t/p/w500/' + element['poster_path']}
            movie_list.append(temp_dict)
        elif element['poster_path'] is None:
            temp_dict = {'id' : element['id'], 'title': element['title'], 'release_date': 'Unknown', 'poster_path': 'https://upload.wikimedia.org/wikipedia/commons/2/2f/QuestionMark.jpg'}
            movie_list.append(temp_dict)
        else:
            temp_dict = {'id' : element['id'], 'title': element['title'], 'release_date': element['release_date'], 'poster_path': 'https://image.tmdb.org/t/p/w500/' + element['poster_path']}
            movie_list.append(temp_dict)

    print(movie_list)

    return movie_list


# TODO: Make it support more than danish & more than flatrate
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
            provider_list.append({'Providers' : 'None in DK'})
    else:
        provider_list.append({'Providers' : 'None in DK'})

    print(provider_list)

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

    print(movie_data)

    return movie_data

