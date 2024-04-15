from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from engl210e_final.auth import login_required

from engl210e_final.db import init_user_db, get_user_db, incr_step, get_token_db

bp = Blueprint('tutorial', __name__)

@bp.route('/', methods=['GET'])
@login_required
def index():
    step = g.user['step']
    return render_template(f'sections/{step}.html')

@bp.route('/', methods=['POST'])
@login_required
def dummy_login():
    step = g.user['step']
    req_type = request.form['type']

    if req_type == "next":
        incr_step()
        return render_template(f'sections/{step + 1}.html')

    username = request.form['username']
    password = request.form['password']
    db = get_user_db(g.user['token'])

    error = None
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
       flash("Success!", True) 
    else:
       flash(error, False)

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

    init_user_db(g.user['token']) 

    return redirect(url_for('index'))