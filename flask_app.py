
import sqlite3
import os
import json
from flask import Flask, g

app = Flask(__name__)

#TOKEN_DB = os.getenv('PWD') + '/dbs/token.db'
TOKEN_DB = 'dbs/token.db'
USER_DB = None

def query_token_db(query, args = (), one = False):
    cur = get_token_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def query_db(query, args = (), one = False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def get_token_db():
    db = getattr(g, '_token_database', None)
    if db is None:
        db = g._database = sqlite3.connect(TOKEN_DB)
        db.row_factory = sqlite3.Row
    return db

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(USER_DB)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    token_db = getattr(g, '_token_database', None)
    db = getattr(g, '_database', None)
    if token_db is not None:
        token_db.close()
    if db is not None:
        db.close()

# call this via python shell to initialize the db
def init_token_db():
    if os.path.isfile(TOKEN_DB):
        os.remove(TOKEN_DB)
    f = open(TOKEN_DB, "x").close()

    with app.app_context():
        # create tables
        db = get_token_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

        # add tokens
        # TODO hash them
        tokens = json.loads(open('tokens.json'))
        for t in tokens:
            db.execute(f"insert into Tokens(TOKEN) values ({t})")
        db.commit()
        print('here')
    
@app.route('/')
def hello_world():
    ret = ""
    for x in query_token_db("select * from Tokens"):
        ret += f"{x['ID']} and {x['TOKEN']}"
    return ret


