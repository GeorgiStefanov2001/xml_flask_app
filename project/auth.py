from flask import Blueprint, render_template, redirect, url_for, request, flash
import bcrypt

from . import db
from .models import User

auth = Blueprint("auth", __name__)


@auth.route("/login")
def login():
    return render_template("login.html")


@auth.route("/signup")
def signup():
    return render_template("signup.html")


@auth.route("/signup", methods=["POST"])
def signup_post():
    email = request.form.get("email")

    user = User.query.filter_by(
        email=email
    ).first()  # if this returns a user, then the email already exists in database

    # if a user is found, email already exists in the db
    # redirect back to signup page so user can try again

    if user:
        flash("Email address already exists.")
        return redirect(url_for("auth.signup"))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.

    # generate salt for password
    salt = bcrypt.gensalt()

    new_user = User(
        email=email,
        username=request.form.get("username"),
        password=bcrypt.hashpw(bytes(request.form.get("password"), "utf-8"), salt),
        firstname=request.form.get("firstname"),
        lastname=request.form.get("lastname"),
    )

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for("auth.login"))


@auth.route("/logout")
def logout():
    return "Logout"
