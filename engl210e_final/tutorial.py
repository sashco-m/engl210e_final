from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from engl210e_final.auth import login_required

from engl210e_final.db import init_user_db, get_user_db, incr_step, get_token_db

bp = Blueprint('tutorial', __name__)

# pages for
# - ethics statement
# - main text / login screen

# probably just return a page with a big blob of text that can be cycled through
# successfully performing the injection can lead to another page idk
# be sure to wrap the hell out of the input with try-except

@bp.route('/', methods=('GET', 'POST'))
@login_required
def index():
    step = g.user['step']

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_user_db(g.user['token'])
        error = None
        dummy_user = db.execute(
            'SELECT * FROM Users WHERE username = ?', (username,)
        ).fetchone()

        if dummy_user is None:
            error = 'Incorrect username.'
        elif dummy_user['password'] != password:
            error = 'Incorrect password.'

        if error is None:
           # progress the tutorial
           incr_step()
           return render_template(f'sections/{step + 1}.html')

        flash(error)

    return render_template(f'sections/{step}.html')

@bp.route('/ethics', methods=('GET', 'POST'))
@login_required
def ethics():
    if request.method == 'POST':
        return redirect(url_for('index'))

    if g.user['step'] != 1:
        return redirect(url_for('index'))

    return render_template('ethics.html')

@bp.route('/reset')
@login_required
def reset():
    if 'user' not in g:
        raise 'no user'

    db = get_token_db()
    db.execute(f'update Tokens set step = 1 where id = {g.user["id"]}')
    db.commit()

    return redirect(url_for('index'))