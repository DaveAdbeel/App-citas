from flask import Flask
from flask_mysqldb import MySQL, MySQLdb

from config import _DB, _HOST, _PASSWORD, _SECRET_KEY, _USER
from routes.app_routes import Routes

app = Flask(__name__)

app.config["MYSQL_HOST"] = _HOST
app.config["MYSQL_USER"] = _USER
app.config["MYSQL_PASSWORD"] = _PASSWORD
app.config["MYSQL_DB"] = _DB
app.config["SECRET_KEY"] = _SECRET_KEY

mysql = MySQL(app)

app.register_blueprint(Routes)

if __name__ == "__main__":
    app.run(debug=True)
