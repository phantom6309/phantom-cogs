import aiohttp
from imdb import IMDb

ia = IMDb()  # Initialize IMDbPY instance

async def get_trakt_user_activity(username, access_token):
    url = f'https://api.trakt.tv/users/{username}/history'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}',
        'trakt-api-version': '2',
        'trakt-api-key': access_token  # Replace with actual key if needed
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                return await response.json()
            else:
                return None

def extract_title_and_imdb_id(activity_item):
    if 'movie' in activity_item:
        title = activity_item['movie']['title']
        imdb_id = activity_item['movie']['ids'].get('imdb', '')
        return title, imdb_id
    elif 'episode' in activity_item and 'show' in activity_item:
        title = f"{activity_item['show']['title']} - {activity_item['episode']['title']}"
        return title, None
    elif 'show' in activity_item:
        title = activity_item['show']['title']
        return title, None
    return 'Unknown Title', None

async def get_imdb_info(imdb_id):
    try:
        movie = ia.get_imdbID(imdb_id)
        movie_data = ia.get_movie(movie.movieID)
        return {
            'title': movie_data.get('title'),
            'plot': movie_data.get('plot', [''])[0],
            'poster': movie_data.get('cover url'),
            'year': movie_data.get('year'),
            'genres': ', '.join(movie_data.get('genres', [])),
            'rating': movie_data.get('rating')
        }
    except Exception as e:
        print(f"Error retrieving IMDb info: {e}")
        return None
