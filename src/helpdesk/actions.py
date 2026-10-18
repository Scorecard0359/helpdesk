from sqlalchemy import exc

from helpdesk.db import db
from helpdesk.models import User, Client, Ticket

def get_users():
    result = db.session.execute(
        db.select(User)
    ).scalars().all()

    return result

def get_user(id):
    result = db.session.execute(
        db.select(User).where(User.id == id)
    ).scalar_one()

    return result

def get_clients():
    result = db.session.execute(
        db.select(Client)
    ).scalars().all()

    return result

def get_client(id):
    result = db.session.execute(
        db.select(Client).where(Client.id == id)
    ).scalar_one()

    return result

def get_ticket(id):
    result = db.session.execute(
        db.select(Ticket).where(Ticket.id == id).options(db.joinedload(Ticket.assignee)).options(db.joinedload(Ticket.client))
    ).scalar_one()

    return result

def get_tickets():
    result = db.session.execute(
        db.select(Ticket).options(db.joinedload(Ticket.assignee)).options(db.joinedload(Ticket.client)).order_by(Ticket.created_at.desc())
    ).scalars().all()

    return result

def add_client(name):
    try:
        client = Client(
            name=name
        )
        db.session.add(client)
        db.session.commit()
    except exc.IntegrityError:
        return 1
    return 0

def delete_client(id):
    db.session.execute(
        db.delete(Client).where(Client.id == id)
    )
    db.session.commit()

def add_ticket(assignee_id, client_id, title, body, sent_via):
    ticket = Ticket(
        assignee_id=assignee_id,
        client_id=client_id,
        title=title,
        body=body,
        sent_via=sent_via
    )
    db.session.add(ticket)
    db.session.commit()

    return ticket.id
