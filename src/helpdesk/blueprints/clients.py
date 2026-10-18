from flask import Blueprint, render_template, redirect, url_for, request

from helpdesk.db import db
from helpdesk.blueprints.auth import login_required, admin_required
from helpdesk.actions import get_clients, add_client, delete_client

bp = Blueprint("clients", __name__, static_folder='static', url_prefix='/clients')

@bp.route("/")
@login_required
def list():
    error = request.args.get('error')
    clients = get_clients()

    return render_template('clients/list.html', clients=clients, error=error)

@bp.route("/add", methods=('GET', 'POST'))
@login_required
@admin_required
def add():
    error = None
    if request.method == 'POST':
        name = request.form['client-name'].strip()

        c = add_client(name)
        if c == 1:
            error = 1
    
    return redirect(url_for("clients.list", error=error))

@bp.route("/delete/<int:id>")
@login_required
@admin_required
def delete(id):
    delete_client(id)

    return redirect(url_for('clients.list'))
