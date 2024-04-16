from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, Response
)
from werkzeug.exceptions import abort

from engl210e_final.auth import login_required

from engl210e_final.db import init_user_db, get_user_db, incr_step, decr_step, get_token_db

bp = Blueprint('tutorial', __name__)

@bp.route('/', methods=['GET'])
@login_required
def index():
    return render_template('tutorial.html', step=g.user['step'])

@bp.route('/', methods=['POST'])
@login_required
def dummy_login():
    # last step stored in DB
    step = g.user['step']

    username = request.form['username']
    password = request.form['password']
    db = get_user_db(g.user['token'])

    error = None
    dummy_user = None
    # intentional SQL injection
    # try/catch sql errors
    try:
        dummy_user = db.execute(
            f'SELECT * FROM Users WHERE username = "{username}" and password = "{password}"'
        ).fetchone()

        if dummy_user is None:
            error = 'Incorrect username/password.'
    except:
        error = "Invalid SQL Query"

    if error is None:
       flash(f"Success! Welcome, {dummy_user['username']}", True) 
    else:
       flash(error, False)

    return render_template('tutorial.html', step=step)

@bp.route('/next-step', methods=['POST'])
@login_required
def next():
    incr_step()
    return Response()

@bp.route('/prev-step', methods=['POST'])
@login_required
def prev():
    decr_step()
    return Response()

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

    init_user_db(g.user['token']) 

    return redirect(url_for('index'))