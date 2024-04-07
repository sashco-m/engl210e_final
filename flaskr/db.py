import sqlite3

import click
import json
from flask import current_app, g
from werkzeug.security import check_password_hash, generate_password_hash

def get_token_db():
    if 'token_db' not in g:
        g.token_db = sqlite3.connect(
            current_app.config['TOKEN_DB'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.token_db.row_factory = sqlite3.Row

    return g.token_db

def close_db(e=None):
    token_db = g.pop('token_db', None)

    if token_db is not None:
        token_db.close()

def init_token_db():
    db = get_token_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

    with current_app.open_resource('tokens.json') as f:
        tokens = json.load(f)
        for t in tokens:
            hashed_token = generate_password_hash(t) 
            db.execute(f'insert into Tokens(TOKEN) values ("{hashed_token}")')


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_token_db()

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)