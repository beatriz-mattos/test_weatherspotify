from urllib.parse import urlencode
from flask import Blueprint, redirect, request, jsonify
import base64
import requests
from app.config import Config

blueprint = Blueprint('auth', __name__)

@blueprint.route('/login', methods=['GET'])
def login():
    state = 'random_state'
    scope = 'user-read-private user-read-email'
    auth_url = 'https://accounts.spotify.com/authorize?' + urlencode({
        'response_type': 'code',
        'client_id': Config.SPOTIFY_CLIENT_ID,
        'scope': scope,
        'redirect_uri': Config.SPOTIFY_REDIRECT_URI,
        'state': state
    })
    return redirect(auth_url)

@blueprint.route('/callback', methods=['GET'])
def callback():
    code = request.args.get('code')
    state = request.args.get('state')

    if state is None:
        return jsonify({'error': 'State mismatch'}), 400

    token_url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': 'Basic ' + base64.b64encode(f'{Config.SPOTIFY_CLIENT_ID}:{Config.SPOTIFY_CLIENT_SECRET}'.encode()).decode('utf-8'),
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'code': code,
        'redirect_uri': Config.SPOTIFY_REDIRECT_URI,
        'grant_type': 'authorization_code'
    }

    response = requests.post(token_url, headers=headers, data=data)
    token_data = response.json()

    if response.status_code != 200:
        return jsonify({'error': 'Unable to fetch access token'}), response.status_code

    return jsonify(token_data)
