import click
from flask import Flask
from werkzeug.security import generate_password_hash

from helpdesk.db import db
from helpdesk.models import User
from helpdesk.blueprints import misc, auth

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI="sqlite:///helpdesk.db",
        INVITE_ONLY=False,
    )

    app.register_blueprint(auth.bp)
    app.register_blueprint(misc.bp)

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

    return app
