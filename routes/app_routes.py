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
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        interest_sex = request.form["interest_sex"]
        user_type = request.form["user_type"]

        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        
        
        
        msg = User.insert_user(
            {"nombre": username, "email": email, "interest_sex": interest_sex, "user_type": user_type, "password": hashed_password}
        )
        
        if msg != 200:
            flash(msg)
        else:
            flash("Cuenta creada con exito!")
            isAccountCreated = True
        

    sexes = Interest_Sex.get_all()
    user_types = User_Type.get_all()
    messages= get_flashed_messages()
    
    return render_template("register.html", sexes=sexes, user_types=user_types, messages=messages, isAccountCreated=isAccountCreated)
