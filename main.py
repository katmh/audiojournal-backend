import os
from flask import Flask, request, render_template, redirect, url_for
import sqlalchemy
import json

app = Flask(__name__)

db = sqlalchemy.create_engine(
    sqlalchemy.engine.url.URL(
        drivername='mysql+pymysql',
        username="service",
        password="service",
        database="journal",
        query={
            'unix_socket': '/cloudsql/audiojournal:us-east1:journal-db'
        }
    ),

    pool_size=5,
    max_overflow=2,
    pool_timeout=30,
    pool_recycle=1800,

)

# @app.route('/new_record', methods=['POST'])
# def new_record():

#     entry = Entry(name=request.json.name, summary="", keywords="", transcript="", tags="", location=request.json.location)
#     db.collection(u'entries').add(entry.to_dict())
#     return redirect(url_for('view'))

@app.route('/view', methods=['GET'])
def view_all():
    entry_list = []
    with db.connect() as conn:
        entries = conn.execute(
            "SELECT * FROM journal.entries"
        ).fetchall()
        for row in entries:
            entry_list.append(row)


    return render_template('index.html', data=entry_list)

@app.route('/map', methods=['GET'])
def view_all():
    entry_list = []
    with db.connect() as conn:
        entries = conn.execute(
            "SELECT * FROM journal.entries"
        ).fetchall()
        for row in entries:
            entry_list.append(row)
    return render_template('map.html', data=entry_list)
