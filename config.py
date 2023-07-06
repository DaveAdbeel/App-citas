import os

from dotenv import load_dotenv

load_dotenv()

_USER = os.getenv("MYSQL_USER")
_PASSWORD = os.getenv("MYSQL_PASSWORD")
_HOST = os.getenv("MYSQL_HOST")
_DB = os.getenv("MYSQL_DB")
_SECRET_KEY = os.getenv("SECRET_KEY")

class config_app():
    def __init__(self, app, route):
        app.config["SECRET_KEY"] = _SECRET_KEY            
        app.register_blueprint(route)