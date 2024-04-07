import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from engl210e_final.db import get_token_db

bp = Blueprint('auth', __name__, url_prefix='/')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        token = request.form['token']
        db = get_token_db()
        error = None

        rows = db.execute('select * from Tokens').fetchall()
        result = None
        for row in rows:
            if check_password_hash(row['token'], token):
                result = row
                break

        if result is None:
            error = 'Incorrect token.'

        if error is None:
            session.clear()
            session['user_id'] = result['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_token_db().execute(
            'SELECT * FROM Tokens WHERE id = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view