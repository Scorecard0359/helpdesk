from flask import Blueprint, render_template, redirect, url_for

from helpdesk.blueprints.auth import login_required
from helpdesk.actions import get_users

bp = Blueprint("users", __name__, static_folder='static', url_prefix='/users')

@bp.route("/")
@login_required
def index():
    return redirect(url_for("users.list"))

@bp.route("/list")
@login_required
def list():
    users = get_users()

    return render_template('users/list.html', users=users)
