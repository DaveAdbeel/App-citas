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

from models.comments import Comments
from models.discussions import Discussions
from models.interest_sex import Interest_Sex
from models.like_users import Like_Users
from models.user import User
from models.user_type import User_Type

startup_routes = Blueprint("startup_routes", __name__)

bcrypt = Bcrypt()
#middelware
@startup_routes.before_request
def middleware():
    g.user = None
    
    if 'user' in session:
        g.user = session["user"]

#main routes
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
    if g.get("user"):        
        discussions = Discussions.filter_discussions(Discussions.get_all_discussions())
        
        
        return render_template("home.html", user=session["user"], discussions=discussions, is_user_liked=Like_Users.is_user_liked)
    return redirect(url_for("startup_routes.index"))
#user routes 
@startup_routes.route("/my_profile", methods=["GET", "POST"])
def my_profile(): 
    if g.get("user"):
        session["user"] = User.get_user(session["user"]["email"])    
        
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


@startup_routes.route("/account/<uid>")
def user_account(uid):
    if g.get("user"):
        if int(session["user"]["id"]) == int(uid):
            return redirect(url_for("startup_routes.my_profile"))
        
        user = User.get_user_with_uid(uid)
        return render_template("components/account_profile.html", user=user)

#Discussions and comments routes
@startup_routes.route("/like", methods=["POST"])
def like():
    if g.get("user"):
        if request.method == "POST":
            data = request.get_json()
            Like_Users.handleLike(data["opt"], data["user_id"], data["table"], data["post_id"], session["user"]["id"])
            return {"status": 200}
    
    

@startup_routes.route("/add_discussion", methods=["POST"])
def add_discussion():
    if g.get("user"):
        if request.method == "POST":
            title = request.form["title_discussion"]
            Discussions.insert_discussion({'user_id': g.user["id"], 'title': title })
            return redirect(url_for("startup_routes.home"))
        
@startup_routes.route("/delete_discussion/<uid>")
def delete_discussion(uid):
    if g.get("user"):
        Discussions.delete_discussion(uid)
        return redirect(url_for("startup_routes.home"))
        
@startup_routes.route("/edit_discussion/<uid>", methods=["GET", "POST"])
def edit_discussion(uid):
    if g.get("user"):
        if request.method == "POST":
            new_title = request.form["content"]
            Discussions.edit_discussion(uid, new_title)
            return redirect(url_for("startup_routes.home"))
        
        title_discussion = Discussions.get_discussion(uid)["titulo"]
        return render_template("components/edit.html",edit_type="discusion",uid=uid, content=title_discussion, route="edit_discussion")
        


@startup_routes.route('/edit_comment/<uid>', methods=['GET', 'POST'])
def edit_comment(uid):
    if g.get("user"):
        if request.method == "POST":
            new_content = request.form["content"]
            Comments.edit_comment(uid, new_content)
            return redirect(url_for("startup_routes.home"))
        
        content_comment = Comments.get_comment(uid)["contenido"]
        return render_template("components/edit.html",edit_type="comentario",uid=uid, content=content_comment, route="edit_comment")

@startup_routes.route('/delete_comment/<uid>')
def delete_comment(uid):
   if g.get("user"):
        Comments.delete_comment(uid)
        return redirect(url_for("startup_routes.home"))


@startup_routes.route('/add_comment/<uid>', methods=['POST'])
def add_comment(uid):
    if g.get("user"):
        if request.method == "POST":
            content = request.form["comentario"]
            Comments.insert_comment({'discussion_id': uid, 'user_id': g.user["id"], 'content': content })
            return redirect(url_for("startup_routes.home"))
