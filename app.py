from flask import Flask
from flask_bcrypt import Bcrypt

from config import config_app
from routes.app_routes import Routes

app = Flask(__name__)
bcrypt = Bcrypt(app)

config_app(app, Routes)

if __name__ == "__main__":
    app.run(debug=True)
