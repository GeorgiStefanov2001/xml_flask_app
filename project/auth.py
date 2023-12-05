import bcrypt
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user

from . import db
from .models import User

auth = Blueprint("auth", __name__)


@auth.route("/login")
def login():
    return render_template("login.html")


@auth.route("/login", methods=["POST"])
def login_post():
    username = request.form.get("username")
    password = request.form.get("password")

    user = User.query.filter_by(username=username).first()

    flash_msg = ""
    if not user:
        flash_msg = "Invalid username - user doesn't exist."
    else:
        # check if password is correct
        hashed_pass = user.password
        password_correct = (
            bcrypt.hashpw(bytes(password, "utf-8"), hashed_pass) == hashed_pass
        )
        flash_msg = flash_msg if password_correct else "Incorrect password."

    if flash_msg != "":
        flash(flash_msg)
        return redirect(url_for("auth.login"))

    # credentials are correct - log user in
    login_user(user, remember=(True if request.form.get("remember") else False))
    return redirect(url_for("main.profile"))


@auth.route("/signup")
def signup():
    return render_template("signup.html")


@auth.route("/signup", methods=["POST"])
def signup_post():
    email = request.form.get("email")
    username = request.form.get("username")

    user = User.query.filter_by(email=email).first()

    # if a user is found, email already exists in the db
    # redirect back to signup page so user can try again

    if user:
        flash("Email address already exists")
        return redirect(url_for("auth.signup"))
    else:
        user = User.query.filter_by(username=username).first()
        if user:
            flash("Username already exists")
            return redirect(url_for("auth.signup"))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(
        email=email,
        username=username,
        password=bcrypt.hashpw(
            bytes(request.form.get("password"), "utf-8"), bcrypt.gensalt()
        ),
        firstname=request.form.get("firstname"),
        lastname=request.form.get("lastname"),
    )

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for("auth.login"))


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))
