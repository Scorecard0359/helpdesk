from flask import Blueprint, render_template, redirect, url_for, request

from helpdesk.blueprints.auth import login_required, admin_required
from helpdesk.actions import get_clients, get_users, get_tickets, add_ticket, get_ticket, get_user, get_client, ticket_change_status, ticket_change_assignee, ticket_change_discussion, ticket_change_priority

bp = Blueprint("tickets", __name__, static_folder='static', url_prefix='/tickets')

@bp.route("/")
@login_required
def list():
    tickets = get_tickets()

    return render_template('tickets/list.html', tickets=tickets)

@bp.route("/<int:id>")
@login_required
def show(id):
    ticket = get_ticket(id)
    users = get_users()

    return render_template('tickets/show.html', ticket=ticket, users=users)

@bp.route("/add", methods=('GET', 'POST'))
@login_required
def add():
    users = get_users()
    clients = get_clients()
    error = None

    if request.method == 'POST':
        assignee = request.form['assignee']
        client = request.form['client']
        title = request.form['title'].strip()
        body = request.form['body'].strip()
        publish_method = request.form['publish_method']

        try:
            if not client or int(client) <= 0:
                error = "Выберите клиента."
            elif not body or not title:
                error = "Заполните заявку."
            elif int(publish_method) > 3 or int(publish_method) < 0:
                error = "Выберите корректный способ регистрации."
            elif len(body) < 100:
                error = "Развёрнуто заполните заявку."
            elif get_user(int(assignee)) is None:
                error = "Выберите корректного ответственного."
            elif get_client(int(client)) is None:
                error = "Выберите корректного клиента."
            else:
                ticket = add_ticket(assignee, client, title, body, publish_method)

                return redirect(url_for('tickets.show', id=ticket))
        except Exception:
            error = "Непредвиденная ошибка."

    return render_template('tickets/add.html', clients=clients, users=users, error=error)

@bp.route("/chstatus/<int:id>")
@login_required
def change_status(id):
    ticket = get_ticket(id)

    if ticket:
        ticket_change_status(id)

    return redirect(url_for("tickets.show", id=id))

@bp.route("/chassignee", methods=('GET', 'POST'))
@login_required
def change_assignee():
    if request.method == "POST":
        id = int(request.form['id'])
        ticket = get_ticket(id)
        user = get_user(int(request.form['user']))

        if ticket and user:
            ticket_change_assignee(id, user.id)

        return redirect(url_for("tickets.show", id=id))

    return redirect(url_for("tickets.list"))

@bp.route("/chpriority", methods=('GET', 'POST'))
@login_required
def change_priority():
    if request.method == "POST":
        id = int(request.form['id'])
        ticket = get_ticket(id)
        priority = int(request.form['priority'])

        if ticket and priority:
            if not priority < 1 and priority <= 3:
                ticket_change_priority(id, priority)

        return redirect(url_for("tickets.show", id=id))

    return redirect(url_for("tickets.list"))

@bp.route("/chdiscussion/<int:id>")
@login_required
@admin_required
def change_discussion(id):
    ticket = get_ticket(id)

    if ticket:
        ticket_change_discussion(id)

    return redirect(url_for("tickets.show", id=id))
