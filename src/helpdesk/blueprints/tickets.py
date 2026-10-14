from flask import Blueprint, render_template, redirect, url_for, request

from helpdesk.blueprints.auth import login_required
from helpdesk.actions import get_clients, get_users, get_tickets, add_ticket, get_ticket

bp = Blueprint("tickets", __name__, static_folder='static', url_prefix='/tickets')

@bp.route("/")
@login_required
def index():    
    return redirect(url_for("tickets.list"))

@bp.route("/list")
@login_required
def list():
    tickets = get_tickets()

    return render_template('tickets/list.html', tickets=tickets)

@bp.route("/<int:id>")
@login_required
def show(id):
    ticket = get_ticket(id)

    return render_template('tickets/show.html', ticket=ticket)

@bp.route("/add", methods=('GET', 'POST'))
@login_required
def add():
    users = get_users()
    clients = get_clients()

    if request.method == 'POST':
        assignee = request.form['assignee']
        client = request.form['client']
        title = request.form['title'].strip()
        body = request.form['body'].strip()
        publish_method = request.form['publish_method']

        add_ticket(assignee, client, title, body, publish_method)

        return redirect(url_for('tickets.list'))

    return render_template('tickets/add.html', clients=clients, users=users)
