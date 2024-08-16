from flask import Flask, request, jsonify, redirect
import requests
import base64
import os
from dotenv import load_dotenv
from urllib.parse import urlencode
from flask_caching import Cache

load_dotenv()

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

# API config
OPENWEATHERMAP_API_KEY = os.getenv('OPENWEATHERMAP_API_KEY')
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
SPOTIFY_REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')

@cache.cached(timeout=300, key_prefix='weather')
def get_weather(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHERMAP_API_KEY}&units=metric'
    response = requests.get(url)
    data = response.json()
    if response.status_code != 200:
        raise Exception(f"Error fetching weather data: {data}")
    return data

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

@app.route('/login', methods=['GET'])
def login():
    state = 'random_state'  # Generate a random state for security
    scope = 'user-read-private user-read-email'
    auth_url = 'https://accounts.spotify.com/authorize?' + urlencode({
        'response_type': 'code',
        'client_id': SPOTIFY_CLIENT_ID,
        'scope': scope,
        'redirect_uri': SPOTIFY_REDIRECT_URI,
        'state': state
    })
    return redirect(auth_url)

@app.route('/callback', methods=['GET'])
def callback():
    code = request.args.get('code')
    state = request.args.get('state')

    if state is None:
        return jsonify({'error': 'State mismatch'}), 400

    token_url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': 'Basic ' + base64.b64encode(f'{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}'.encode()).decode('utf-8'),
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'code': code,
        'redirect_uri': SPOTIFY_REDIRECT_URI,
        'grant_type': 'authorization_code'
    }
    
    response = requests.post(token_url, headers=headers, data=data)
    token_data = response.json()
    
    if response.status_code != 200:
        return jsonify({'error': 'Unable to fetch access token'}), response.status_code
    
    return jsonify(token_data)

@cache.cached(timeout=60)
@app.route('/playlist', methods=['GET'])
def playlist():
    city = request.args.get('city')
    refresh_token = request.args.get('refresh_token')
    
    if not city or not refresh_token:
        return jsonify({'error': 'City and refresh_token are required'}), 400

    # Get the current temperature
    weather_data = get_weather(city)
    temperature = weather_data['main']['temp']
    
    # Determines music genre based on temperature
    if temperature > 25:
        genre = 'pop'
    elif 10 <= temperature <= 25:
        genre = 'rock'
    else:
        genre = 'classical'
    
    # Get a new access token using refresh token
    token_url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': 'Basic ' + base64.b64encode(f'{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}'.encode()).decode('utf-8'),
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
    
    # Get a playlist from Spotify
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
        },
        # 'full_log': playlist_data
    }
    
    return jsonify(formatted_playlist_data)

if __name__ == '__main__':
    app.run(debug=True, port=8888)
