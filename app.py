from flask import Flask
from flask_bcrypt import Bcrypt

from config import config_app
from routes.startup_routes import startup_routes

app = Flask(__name__)
bcrypt = Bcrypt(app)

config_app(app, startup_routes)


if __name__ == "__main__":
    app.run(debug=True)
