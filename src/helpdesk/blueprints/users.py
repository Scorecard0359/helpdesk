from flask import Blueprint, render_template, redirect, url_for

from helpdesk.blueprints.auth import login_required, admin_required, invite_mode_enabled
from helpdesk.actions import get_users, get_invite_codes, create_invite_code, delete_invite_code

bp = Blueprint("users", __name__, static_folder='static', url_prefix='/users')

@bp.route("/")
@login_required
def list():
    users = get_users()

    return render_template('users/list.html', users=users)

@bp.route("/invites")
@login_required
@invite_mode_enabled
def invite_list():
    invites = get_invite_codes()

    return render_template('users/invites.html', invites=invites)

@bp.route("/invites/create")
@login_required
@admin_required
@invite_mode_enabled
def invite_create():
    create_invite_code()

    return redirect(url_for("users.invite_list"))

@bp.route("/invites/delete/<int:id>")
@login_required
@admin_required
@invite_mode_enabled
def invite_delete(id):
    delete_invite_code(id)

    return redirect(url_for("users.invite_list"))
