
# A very simple Flask Hello World app for you to get started with...
import sqlite3
import os
from flask import Flask, g

app = Flask(__name__)

DATABASE = os.getenv('BASE_PATH') + '/dbs/test.db'


def query_db(query, args = (), one = False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# call this via python shell to initialize the db
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.route('/')
def hello_world():
    query_db("insert into Test values(1,'bruh')")
    ret = ""
    for x in query_db("select * from test"):
        ret += f"{x['ID']} and {x['Msg']}"
    # return 'Work in progess: ENGL210E final project'
    return ret