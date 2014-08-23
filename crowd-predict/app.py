# coding:utf-8
import os
from cgi import escape
from collections import Counter
from urlparse import urlparse
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask.ext.seasurf import SeaSurf
from flask.ext.bcrypt import Bcrypt
from flask.ext.gravatar import Gravatar
from mongoengine import connect
import json

import settings
from models import *


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


def get_current_profile():
    profile = Profile.objects(email='acccko@gmail.com').first()
    return profile


@app.route("/")
def home_page():
    ''' redirects to event page '''
    return redirect(url_for('events_page'))

@app.route("/events/")
def events_page():
    ''' list of events '''
    events = Event.objects.all()
    return render_template('events.html', events=events)

@app.route("/event/<event_key>/")
def event_page(event_key, methods=[u'GET', 'POST']):
    ''' event data '''
    if request.method == 'POST':  # updating prediction
        profile = get_current_profile()
        return redirect(url_for('events_page', event_key=event_key))
    else:
        event_key = escape(event_key)
        event = Event.objects(event_key=event_key).first()
        profile_events = ProfileEvent.objects.filter(event=event_key)
        cntr = Counter()
        for pe in profile_events:
            for a in pe.answers:
                cntr[a] += 1
        answers_stat = [{'answer': k, 'score': v} for k,v in dict(cntr).items()]

        return render_template('event.html', event=event, profile_events=profile_events)


@app.route("/api/event/<event_key>/")
def event_page(event_key):
    ''' event data '''
    event_key = escape(event_key)
    event = Event.objects(event_key=event_key).first()
    profile_events = ProfileEvent.objects.filter(event=event_key)
    cntr = Counter()
    for pe in profile_events:
        for a in pe.answers:
            cntr[a] += 1
    answers_stat = [{'answer': k, 'score': v} for k,v in dict(cntr).items()]

    return json.dumps(answers_stat)