import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash

import click
from flask import current_app, g

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

def add_superuser(username: str, password: str):
    db = get_db()

    if not db:
        print("База данных не была инициализирована.")
    elif db.execute('SELECT * FROM users WHERE username = ?', (username,)):
        print(f"Пользователь {username} уже существует. Вы можете сделать его суперпользователем сменой параметра is_admin.")
    else:
        db.execute("INSERT INTO user (username, password) VALUES (?, ?)", (username, generate_password_hash(password)),)
        db.commit()
        print(f"Суперпользователь {username} был создан.")

@click.command('init-db')
@click.option('--force', help='Принудительно пересоздать базу данных.')
def init_db_command(force):
    db = get_db()

    if db and db.execute('SELECT * FROM users') is not None and not force:
        print("База данных не является пустой. Добавьте к команде '--force' для принудительной инициализации.")
    else:
        init_db()
        print("База данных инициализирована.")

sqlite3.register_converter(
    "timestamp", lambda v: datetime.fromisoformat(v.decode())
)

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
