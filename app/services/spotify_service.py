import requests
from flask import request
from app.config import Config

@cache.cached(timeout=300, key_prefix=lambda: f'spotify_playlists_{request.args.get("access_token")}_{request.args.get("genre")}')
def get_spotify_playlists(access_token, genre):
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    url = f'https://api.spotify.com/v1/recommendations?seed_genres={genre}'
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Error fetching playlist data: {response.json()}")
    return response.json()
