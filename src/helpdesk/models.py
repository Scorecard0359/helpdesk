from sqlalchemy import Integer, String, ForeignKey, DateTime, Boolean, func
from sqlalchemy.orm import Mapped, mapped_column

class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    full_name: Mapped[str] = mapped_column(String(100), nullable=True)
    status: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    group_id: Mapped[int] = mapped_column(Integer, ForeignKey("groups.id"), nullable=False, default=0)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    registered_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())

class Ticket(db.Model):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    assignee_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    client_name: Mapped[str] = mapped_column(String(100), nullable=False)
    created: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    sent_via: Mapped[int] = mapped_column(Integer, ForeignKey("publish_methods.id"), nullable=False, default=0)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    body: Mapped[str] = mapped_column(String(1000), nullable=True)
    status: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    priority: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    discussion_closed: Mapped[bool] = mapped_column(Boolean, default=False)
    at_review: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

class TicketComment(db.Model):
    __tablename__ = "ticket_comments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    ticket_id: Mapped[int] = mapped_column(Integer, ForeignKey("tickets.id"), nullable=False)
    created: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    body: Mapped[str] = mapped_column(String(1000), nullable=False)
    hidden: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

class Group(db.model):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

class PublishMethod(db.model):
    __tablename__ = "publish_methods"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
