from decouple import config
import json
import requests

api_key = config('THE_MOVIE_DB_API_KEY')
api_url = f'https://api.themoviedb.org/3/movie?api_key={api_key}'

def get_movies(keyword):
    search_api_url = f'https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={keyword}'
    data = requests.get(search_api_url).json()

    titles = [movie['title'] for movie in data['results']]
    release_dates = [movie['release_date'] for movie in data['results']]
    poster = [get_img_url_w500(movie['poster_path']) for movie in data['results']]

    print(poster)

    return data

def get_movie_providers(movie_id):
    pass


def get_img_url_w500(img_url):
    return 'https://image.tmdb.org/t/p/w500' + str(img_url)
