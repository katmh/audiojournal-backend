import os
from flask import Flask, request, render_template
from airtable.airtable import Airtable
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    airtable = Airtable('appnHKrgvz8qkq4ur', 'Entries')

    if request.method == 'POST':
        airtable.insert({'Title': request.args['title']})

        return airtable.get_all()
    else:
        return render_template('index.html', data=airtable.get_all())