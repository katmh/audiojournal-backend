import os
from flask import Flask, request, render_template, redirect, url_for
from entry import Entry
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


@app.route('/new_record', methods=['POST'])
def new_record():
    entry = Entry(name=request.json.name, summary="", keywords="", transcript="", audio_file_url=request.json.audio_file_url, tags="", location=request.json.location)
    db.collection(u'entries').add(entry.to_dict())
    return redirect(url_for('view'))

@app.route('/view', methods=['GET'])
def view_all():
    entries = []
    with db.connect() as conn:
        # Execute the query and fetch all results
        entries = conn.execute(
            "SELECT * FROM journal.entries"
        ).fetchall()
        # Convert the results into a list of dicts representing votes
        for row in entries:
            entries.append(Entry(row[1], row[2], json.loads(row[3]), row[4], json.loads(row[5]), row[6]))


    return render_template('index.html', data=entries)
    )
    return 