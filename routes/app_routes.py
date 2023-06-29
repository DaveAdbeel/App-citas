from flask import (
    Blueprint,
    flash,
    get_flashed_messages,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_bcrypt import Bcrypt

from models.interest_sex import Interest_Sex
from models.user import User
from models.user_type import User_Type

Routes = Blueprint("routes", __name__)

bcrypt = Bcrypt()


@Routes.route("/")
def home():
    return render_template("content.html")


@Routes.route("/login")
def login():
    return render_template("login.html")


@Routes.route("/register", methods=["GET", "POST"])
def register():
    isAccountCreated = False
    status_msg = {"success": "Cuenta creada con exito!", "error": "Error al crear la cuenta!", "accountIsCreated": "La cuenta ya existe!"}
    status_account = None

    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        interest_sex = request.form["interest_sex"]
        user_type = request.form["user_type"]

        if User.user_exists(email):
            status_account = status_msg["accountIsCreated"]
            isAccountCreated = False
        else:
            hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
            user_data = {
                "nombre": username,
                "email": email,
                "interest_sex": interest_sex,
                "user_type": user_type,
                "password": hashed_password,
            }

            query_status = User.insert_user(user_data)

            if query_status == 200:
                status_account = status_msg["success"]
                isAccountCreated = True
            else:
                status_account = status_msg["error"]
                isAccountCreated = False

    flash(status_account)

    sexes = Interest_Sex.get_all()
    user_types = User_Type.get_all()
    messages = get_flashed_messages()

    return render_template("register.html", sexes=sexes, user_types=user_types, messages=messages, isAccountCreated=isAccountCreated)
