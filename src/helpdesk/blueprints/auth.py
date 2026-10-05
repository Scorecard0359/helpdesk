from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from helpdesk import db

bp = Blueprint("auth", __name__, static_folder='static', url_prefix='/auth')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = db.session_execute(db.select(User).where(User.id == user_id))

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        user = db.session_execute(db.select(User).where(User.username == username))

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
        error = None

        if not username:
            error = 'Требуется ввести имя пользователя.'
        elif not password:
            error = 'Требуется ввести пароль.'

        if error is None:
            try:
                user = User(
                    username=username,
                    password=generate_password_hash(password)
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

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
