from flask import Blueprint, render_template

bp = Blueprint("auth", __name__, static_folder='static', url_prefix='/auth')

@bp.route("/login")
def login():
    return render_template("login.html")
