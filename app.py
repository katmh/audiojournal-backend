import os
from flask import Flask, request
from airtable import Airtable
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        airtable = Airtable('appnHKrgvz8qkq4ur', 'Entries', api_key = os.environ['AIRTABLE_API_KEY'])

        airtable.insert({'Title': request.args['title']})

        return airtable.get_all()[-1]
    else:
        return 'Hello, World!'