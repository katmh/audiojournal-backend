import os
from flask import Flask, request, render_template, redirect, url_for
import sqlalchemy
import json
import textrazor

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

textrazor.api_key = "737f0a9b50f351c7190769d5cc4b584a59b8341fd632a0572892ebb0"
client = textrazor.TextRazor(extractors=["entities", "topics"])
client.set_classifiers(["textrazor_iab_content_taxonomy"])

LANGUAGE = "english"
SENTENCES_COUNT = 4

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
    entry = {
      "name": request.json.name,
      "location": request.json.location,
      "transcript": request.json.transcript
    }

    response = client.analyze(request.args['text'])

    topics = []
    for topic in response.topics():
      if topic.score > 0.9:
        topics.append(topic.label)


    parser = PlaintextParser.from_string(entry.transcript, Tokenizer(LANGUAGE))

    stemmer = Stemmer(LANGUAGE)

    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)

    summary_sentances = []
    for sentence in summarizer(parser.document, SENTENCES_COUNT):
        summary_sentances.append(sentence)


    time_cast = datetime.datetime.utcnow()

    stmt = sqlalchemy.text(
        "INSERT INTO journal.entries (name, time, summary, keywords, transcript, audio_file, tags, location)"
        " VALUES (:name, :time, :summary, :keywords, :transcript, :audio_file, :tags, :location)"
    )

    with db.connect() as conn:
          conn.execute(stmt, name=entry.name, time=time_cast, summary=summary_sentances.join(". "), keywords=json.dumps(topics), transcript=entry.transcript, audio_file=None, tags=json.dumps(["patient"]), location=entry.location)

    return redirect(url_for('view'))

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
