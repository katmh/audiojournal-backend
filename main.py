import os
from flask import Flask, request, render_template, redirect, url_for
from entry import Entry
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

app = Flask(__name__)

cred = credentials.Certificate("/home/kat_m_huang/audio-journal-firebase-admin-sdk.json")
firebase_admin.initialize_app(cred)
firebase_admin.initialize_app(cred, {
  'projectId': "audio-journal",
})

db = firestore.client()

@app.route('/new_record', methods=['POST'])
def new_record():
    entry = Entry(name=request.json.name, summary="", keywords="", transcript="", audio_file_url=request.json.audio_file_url, tags="", location=request.json.location)
    db.collection(u'entries').add(entry.to_dict())
    return redirect(url_for('view'))

@app.route('/view', methods=['GET'])
def view_all():
    users_ref = db.collection(u'entries')
    docs = users_ref.stream()
    return render_template('index.html', data=[Entry.from_dict(doc.to_dict()) for doc in docs])