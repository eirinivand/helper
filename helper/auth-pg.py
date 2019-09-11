import functools

from sqlalchemy.exc import OperationalError

from helper.app import db
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from helper.models import User
from sqlalchemy import select, insert
from helper.db import get_connection, recreate_database

# from helper.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        # g.user = get_db().execute(
        #     'SELECT * FROM user WHERE id = ?', (user_id,)
        # ).fetchone()
        s = db.create_session()
        g.user = s.execute(select([User]).where(User.id == user_id)).fetchone()


@bp.route('/register', methods=('GET', 'POST'))
# @login_required
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.select([User.id]).where(User.username == username) is None:
            error = 'User {} is already registered.'.format(username)

        try:
            if error is None:
                ins = insert(User).values(username=username, password=generate_password_hash(password))
                get_connection().execute(ins)
                # db.select(
                #     'INSERT INTO user (username, password) VALUES (?, ?)',
                #     (username, generate_password_hash(password))
                # )
                return redirect(url_for('home'))
        except OperationalError:
            print('recreating db')
            recreate_database()
        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        user = get_connection().execute(select([User]).where(User.username == username)).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user.password, password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('home'))

        flash(error)

    return render_template('auth/login.html')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))
