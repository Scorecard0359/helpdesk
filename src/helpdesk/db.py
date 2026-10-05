from datetime import datetime
from werkzeug.security import generate_password_hash

import click
from flask import Flask, current_app, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

@click.command('add-superuser')
def add_superuser(username: str, password: str):
    if db.session_execute(db.select(User).where(User.username == username)):
        print(f"Пользователь {username} уже существует. Вы можете сделать его суперпользователем сменой параметра is_admin.")
    else:
        user = User(
            username=username,
            password=generate_password_hash(password),
            is_admin=True
        )
        db.session.add(user)
        db.session.commit()
        print(f"Суперпользователь {username} был создан.")

def init_app(app):
    app.cli.add_command(add_superuser_command)
