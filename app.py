import os
from flask import Flask, request, render_template
from entry import Entry
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

app = Flask(__name__)

# Use the application default credentials
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
  'projectId': "audio-journal",
})

db = firestore.client()

@app.route('/', methods=['GET', 'POST'])
def index():
    # airtable = Airtable('appnHKrgvz8qkq4ur', 'Entries')

    if request.method == 'POST':
        entry = Entry(name="", summary="", keywords="", transcript="", audio_file_url="", tags="", location="")
        db.collection(u'entries').add(entry.to_dict())
        # airtable.insert({'Title': request.args['title']})

        users_ref = db.collection(u'entries')
        docs = users_ref.stream()

        return [u'{} => {}'.format(doc.id, doc.to_dict()) for doc in docs].join("\n")
    else:
        users_ref = db.collection(u'entries')
        docs = users_ref.stream()
        return render_template('index.html', data=[Entry.from_dict(doc.to_dict()) for doc in docs])