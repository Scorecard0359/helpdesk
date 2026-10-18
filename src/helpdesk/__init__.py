from flask import Flask
from werkzeug.security import generate_password_hash
from babel.dates import format_datetime, format_timedelta
import click, datetime

from helpdesk.db import db
from helpdesk.models import User
from helpdesk.blueprints import auth, clients, tickets, misc, users

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI="sqlite:///helpdesk.db",
        INVITE_ONLY=False,
    )

    app.register_blueprint(auth.bp)
    app.register_blueprint(clients.bp)
    app.register_blueprint(tickets.bp)
    app.register_blueprint(misc.bp)
    app.register_blueprint(users.bp)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.cli.command('add-user', help="Создание пользователя")
    @click.argument('username', help="Имя пользователя", required=True)
    @click.argument('password', help="Пароль", required=True)
    @click.argument('is_admin', default=0)
    def add_superuser(username: str, password: str, is_admin: int):
        if is_admin > 1:
            print("Неверное значение is_admin.")
        elif db.session.execute(db.select(User).where(User.username == username)).fetchone() is not None:
            print(f"Пользователь {username} уже существует.")
        else:
            user = User(
                username=username,
                password=generate_password_hash(password),
                is_admin=is_admin
            )
            db.session.add(user)
            db.session.commit()
            if is_admin == 0:
                print(f"Пользователь {username} был создан.")
            else:
                print(f"Суперпользователь {username} был создан.")
    
    @app.template_filter()
    def format_date(value):
        if value.tzinfo is None:
            value = value.replace(tzinfo=datetime.timezone.utc)

        value_utc = value.astimezone(datetime.timezone.utc)
        now_utc = datetime.datetime.now(datetime.timezone.utc)
        dif = now_utc - value_utc

        if dif < datetime.timedelta(minutes=1):
            return "только что"
        elif dif < datetime.timedelta(days=7):
            return format_timedelta(dif, locale="ru_RU") + " назад"

        return format_datetime(value, "d MMMM y 'в' HH:mm", locale="ru_RU")

    return app
