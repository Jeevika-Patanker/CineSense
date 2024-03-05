import requests

def get_similar_movies(movie_id, api_key):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}/similar?language=en-US&page=1&api_key={api_key}'
    response = requests.get(url)
    return response.json()


def get_popular_movies(api_key):
    url = f'https://api.themoviedb.org/3/movie/popular?language=en-US&page=1&api_key={api_key}'
    response = requests.get(url)
    popular_movies = response.json()['results']
    return [movie['id'] for movie in popular_movies]

def get_movie_details(movie_id, api_key):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?include_adult=false&language=en-US&api_key={api_key}'
    response = requests.get(url)
    return response.json()

def get_recommendations(movie_ids, api_key):
    recommended_movies = []

    for movie_id in movie_ids:
        similar_movies = get_similar_movies(movie_id, api_key)

        for movie in similar_movies['results'][:10]:
            recommended_movies.append({
                'title': movie['title'],
                'id': movie['id']
            })

    return recommended_movies

# Example usage
api_key = 'b2084cac0164f1d1fb47762399c270af'
movie_ids = [20453, 550, 13, 500]  # Example movie IDs

recommended_movies = get_recommendations(movie_ids, api_key)

def get_top_10_movie_ids(recommended_movies):
    top_10_movie_ids = [movie['id'] for movie in recommended_movies[:10]]
    return top_10_movie_ids

top_10_movie_ids = get_top_10_movie_ids(recommended_movies)
