import os
from datetime import datetime
from urlparse import urlparse
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask.ext.seasurf import SeaSurf
from flask.ext.bcrypt import Bcrypt
from flask.ext.gravatar import Gravatar
from functools import wraps

import settings

from mongoengine import connect, Document, StringField, EmailField, DateTimeField, URLField

app = Flask(__name__)
app.config.from_object(settings)

csrf = SeaSurf(app)
bcrypt = Bcrypt(app)
gravatar = Gravatar(app, size=160, default='mm')

database = urlparse(os.environ.get('MONGOHQ_URL', 'mongodb://localhost/flask-job-board'))

connect(database.path[1:],
        host=database.hostname,
        port=database.port,
        username=database.username,
        password=database.password)

#--------------------------------------------------------

class Event(Document):
    title = StringField(required=True)
    dt = DateTimeField(required=True)
    close_dt = DateTimeField(required=True)
    finish_dt = DateTimeField(required=True)

    meta = {
        'ordering': ['-dt']
    }


@app.route("/")
def home():
    events = Event.objects.all()
    return render_template('events.html', events=events)