from flask import Blueprint, flash, redirect, render_template, request, session, url_for

Routes = Blueprint("routes", __name__)

@Routes.route("/")
def home():
    return render_template("content.html")

@Routes.route("/login")
def login():
    return render_template("login.html")

@Routes.route("/register", methods=['GET', 'POST'])
def register():
    return render_template("register.html")