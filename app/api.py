from decouple import config
import json
import requests

api_key = config('THE_MOVIE_DB_API_KEY')
api_url = f'https://api.themoviedb.org/3/movie?api_key={api_key}'
language_url = '&language=dk'

def get_movie_dict(keyword):
    search_api_url = f'https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={keyword}' + language_url
    data = requests.get(search_api_url).json()

    movie_dict = {
    'titles' : [movie['title'] for movie in data['results']],
    'release_dates' : [movie['release_date'] for movie in data['results']],
    'poster_img' : [get_img_url_w500(movie['poster_path']) for movie in data['results']]
    }

    print(movie_dict)

    return movie_dict


def get_movie_providers(movie_id):
    search_api_url = f'https://api.themoviedb.org/3/movie/{movie_id}/watch/providers?api_key={api_key}'+ language_url
    data = requests.get(search_api_url).json()

    print(data['results']['DK']['flatrate'][0]['provider_name'])

    provider_dict = {   
    'provider_name' : [provider['DK']['flatrate'][0]['provider_name'] for provider in data['results']],
    'provider_id' : [provider['DK']['flatrate']['provider_id'] for provider in data['results']],
    'logo_path' : [get_img_url_file_size(provider['DK']['flatrate']['logo_path']) for provider in data['results']]
    }

    print(provider_dict)
    
    return provider_dict


def get_movie_from_id(movie_id):
    pass


def get_img_url_w500(img_url):
    return 'https://image.tmdb.org/t/p/w500' + str(img_url)


def get_img_url_file_size(img_url):
    return 'https://image.tmdb.org/t/p/file_size' + str(img_url)