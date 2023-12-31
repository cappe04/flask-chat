

from flask import Blueprint, request, make_response, redirect, render_template, url_for

from app.cookies import Cookie
from app.db import DbHandle

bp = Blueprint("auth", __name__)

@bp.route("/login/", methods = ["GET", "POST"])
def login():
    args = request.args.to_dict()

    if request.method == "POST":
        username, password = request.form["username"], request.form["password"]
        if (user_id := DbHandle().get_login(username, password)) is None:
            return render_template(
                "login.html", 
                args=args,
                error_message="Opss! You did something wrong. Im not surprised..."
            )

        endpoint = args.pop("redirect_to", "main.home")
        response = make_response(redirect(url_for(endpoint, **args)))

        Cookie.USER_STATIC.set(response, { "user_id": user_id })
        Cookie.USER_DATA.set(response)

        return response
    
    return render_template("login.html", args=args)