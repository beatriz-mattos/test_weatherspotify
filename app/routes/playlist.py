import base64
from flask import Blueprint, request, jsonify
from app.services.weather_service import get_weather
from app.services.spotify_service import get_spotify_playlists
from app.config import Config
import requests

blueprint = Blueprint('playlist', __name__)

@blueprint.route('/playlist', methods=['GET'])
def playlist():
    city = request.args.get('city')
    refresh_token = request.args.get('refresh_token')

    if not city or not refresh_token:
        return jsonify({'error': 'City and refresh_token are required'}), 400

    weather_data = get_weather(city)
    temperature = weather_data['main']['temp']

    if temperature > 25:
        genre = 'pop'
    elif 10 <= temperature <= 25:
        genre = 'rock'
    else:
        genre = 'classical'

    token_url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': 'Basic ' + base64.b64encode(f'{Config.SPOTIFY_CLIENT_ID}:{Config.SPOTIFY_CLIENT_SECRET}'.encode()).decode('utf-8'),
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }

    token_response = requests.post(token_url, headers=headers, data=data)
    if token_response.status_code != 200:
        return jsonify({'error': 'Unable to fetch access token'}), token_response.status_code

    access_token = token_response.json().get('access_token')
    playlist_data = get_spotify_playlists(access_token, genre)

    formatted_temperature = f"{temperature:.0f}°C"
    formatted_playlist_data = {
        'cidade': city,
        'temperatura': formatted_temperature,
        'sugestao_playlist': {
            'genero': genre,
            'tracks': [
                {
                    'nome': track['name'],
                    'artista': track['artists'][0]['name'],
                    'album': track['album']['name'],
                    'url': track['external_urls']['spotify']
                }
                for track in playlist_data.get('tracks', [])
            ]
        }
    }

    return jsonify(formatted_playlist_data)
