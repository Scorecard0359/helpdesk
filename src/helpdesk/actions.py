from sqlalchemy import exc

from helpdesk.db import db
from helpdesk.models import User, Client, Ticket, TicketComment

def get_users():
    result = db.session.execute(
        db.select(User)
    ).scalars().all()

    return result

def get_user(id):
    result = db.session.execute(
        db.select(User).where(User.id == id)
    ).scalar_one_or_none()

    return result

def get_clients():
    result = db.session.execute(
        db.select(Client)
    ).scalars().all()

    return result

def get_client(id):
    result = db.session.execute(
        db.select(Client).where(Client.id == id)
    ).scalar_one_or_none()

    return result

def get_ticket(id):
    result = db.session.execute(
        db.select(Ticket).where(Ticket.id == id).options(db.joinedload(Ticket.assignee)).options(db.joinedload(Ticket.client))
    ).scalar_one_or_none()

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

def add_ticket_comment(author_id, ticket_id, body):
    comment = TicketComment(
        author_id=author_id,
        ticket_id=ticket_id,
        body=body
    )
    db.session.add(comment)
    db.session.commit()

    return ticket_id

def get_ticket_comments(id):
    result = db.session.execute(
        db.select(TicketComment).where(TicketComment.ticket_id == id, TicketComment.hidden == 0).options(db.joinedload(TicketComment.author))
    ).scalars().all()

    return result

def get_ticket_comment(id):
    result = db.session.execute(
        db.select(TicketComment).where(TicketComment.id == id).options(db.joinedload(TicketComment.author))
    ).scalar_one_or_none()

    return result

def ticket_hide_comment(id):
    db.session.execute(
        db.update(TicketComment).values(hidden=1).where(TicketComment.id == id)
    )
    db.session.commit()

def ticket_change_status(id):
    status = get_ticket(id).status

    status = not status

    db.session.execute(
        db.update(Ticket).values(status=status).where(Ticket.id == id)
    )
    db.session.commit()
    
def ticket_change_priority(id, priority):
    db.session.execute(
        db.update(Ticket).values(priority=priority).where(Ticket.id == id)
    )
    db.session.commit()

def ticket_change_assignee(id, assignee):
    db.session.execute(
        db.update(Ticket).values(assignee_id=assignee).where(Ticket.id == id)
    )
    db.session.commit()

def ticket_change_discussion(id):
    discussion = get_ticket(id).discussion_closed

    discussion = not discussion

    db.session.execute(
        db.update(Ticket).values(discussion_closed=discussion).where(Ticket.id == id)
    )
    db.session.commit()
