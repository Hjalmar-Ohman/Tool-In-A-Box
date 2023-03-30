from flask import abort, jsonify, request
from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask import request

from EmailFunctionality import *

from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity,
)


def test():
    return "ser ut att fungera"


def signUp(db, User, mail):

    if request.method == "POST":
        data = request.get_json()
        email = data.get("email")
        fname = data.get("fname")
        lname = data.get("lname")
        password = data.get("password")

        user = User(email=email, fname=fname, lname=lname, password_hash="")
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        sign_up_mail(mail, user)

        return "Konto registrerat"


def login(db, bcrypt, User):
    if request.method == "POST":
        data = request.get_json()
        inputemail = data.get("email")
        password = data.get("password")

        usr_temp = User.query.filter_by(email=inputemail).first_or_404()

        if (inputemail == usr_temp.email) & (
            bcrypt.check_password_hash(usr_temp.password_hash, password)
        ):

            access_token = create_access_token(identity=inputemail)
            dict = {"token": access_token, "user": usr_temp.seralize()}
            print(dict["user"])
            return jsonify(dict)
        else:

            return jsonify("fel lösenord eller användarnamn"), 401
        return


def delete_user(db, User):
    if request.method == "DELETE":
        data = request.get_json()
        inputemail = data.get("email")
        db.session.delete(User.query.filter_by(email=inputemail).first_or_404())
        db.session.commit()
        return "user deleted"


# @User_page.route("/<int:user_id>/mytools", methods=["GET"])
# def myTools():
#   return
