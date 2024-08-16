from flask import Flask
from flask_caching import Cache
from app.config import Config

cache = Cache()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    cache.init_app(app)
    
    from app.routes import auth, playlist
    app.register_blueprint(auth.blueprint)
    app.register_blueprint(playlist.blueprint)
    
    return app
