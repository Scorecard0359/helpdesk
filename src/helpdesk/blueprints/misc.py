from flask import Blueprint, render_template, redirect, url_for

bp = Blueprint("misc", __name__, static_folder='static')

@bp.route("/")
def index():
    return redirect(url_for("auth.login"))
