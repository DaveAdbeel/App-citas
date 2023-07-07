from flask import (
    Blueprint,
    flash,
    g,
    get_flashed_messages,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_bcrypt import Bcrypt, check_password_hash

from models.interest_sex import Interest_Sex
from models.user import User
from models.user_type import User_Type

startup_routes = Blueprint("startup_routes", __name__)

bcrypt = Bcrypt()

@startup_routes.before_request
def middleware():
    g.user = None
    
    if 'user' in session:
        g.user = session["user"]


@startup_routes.route("/")
def index():
    return render_template("content.html")


@startup_routes.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        status_msg = {
            "incorrectEmail": "El email no existe",
            "incorrectPassword": "Contraseña incorrecta",
        }
        session.pop("username", None)

        email = request.form["email"]
        password = request.form["password"]
        
        
        if not User.user_exists(email):
            flash(status_msg["incorrectEmail"])
        elif not check_password_hash(User.get_passwd_hash(email), password):
            flash(status_msg["incorrectPassword"])
        else:
            session["user"] = User.get_user(email)            
            
            return redirect(url_for("startup_routes.home"))
        
    messages = get_flashed_messages()
    return render_template("login.html", messages=messages)

@startup_routes.route("/register", methods=["GET", "POST"])
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


@startup_routes.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for("startup_routes.index"))


@startup_routes.route("/home", methods=["GET", "POST"])
def home():
    if g.user:
        return render_template("home.html", username=session["user"]["nombre"])
    return redirect(url_for("startup_routes.index"))

@startup_routes.route("/my_profile", methods=["GET", "POST"])
def my_profile():
    if g.user:
        if request.method == "POST":
            user_id = session["user"]["id"]
            username = request.form["name"]
            email = request.form["email"]
            password = request.form["password"]
            if password != "": password = bcrypt.generate_password_hash(password).decode("utf-8")
            User.update_user(user_id, username, email, password)
            session["user"] = User.get_user(email)
            
        return render_template("my_profile.html", user=session["user"])
    return redirect(url_for("startup_routes.index"))