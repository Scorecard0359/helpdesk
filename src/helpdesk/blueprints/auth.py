from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from helpdesk.db import db
from helpdesk.models import User, InviteCode

bp = Blueprint("auth", __name__, static_folder='static', url_prefix='/auth')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = db.session.execute(db.select(User).where(User.id == user_id))

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        user = db.session.execute(db.select(User).where(User.username == username))

        if user is None:
            error = 'Неверное имя пользователя.'
        elif not check_password_hash(user['password'], password):
            error = 'Неверный пароль.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        repeat_password = request.form['repeat_password']
        full_name = request.form['full_name']
        invite_code = request.form['invite_code']
        error = None

        if not username:
            error = 'Требуется ввести имя пользователя.'
        elif not password:
            error = 'Требуется ввести пароль.'
        elif not repeat_password:
            error = 'Повторите пароль.'
        elif not invite_code and Flask.config['INVITE_ONLY']:
            error = 'Введите код регистрации.'
        elif password != repeat_password:
            error = 'Пароль не совпадает.'

        if error is None:
            if Flask.config['INVITE_ONLY'] and db.session.execute(db.select(InviteCode).where(InviteCode.code == invite_code)).fetchone() is None:
                error = 'Данный код не существует.'
            else:
                try:
                    password = generate_password_hash(password)
                    user = User(
                        username=username,
                        password=password,
                        full_name=full_name,
                        invite_code=invite_code
                    )
                    db.session.add(user)
                    db.session.commit()
                except db.IntegrityError:
                    error = f"Пользователь {username} уже существует."
                else:
                    return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

@bp.route('/')
def index():
    if g.user is None:
        return redirect(url_for('auth.login'))
    else:
        return redirect(url_for('misc.index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
