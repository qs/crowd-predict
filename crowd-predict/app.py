# coding:utf-8
import os
from cgi import escape
from collections import Counter
from urlparse import urlparse
from flask import Flask, render_template, request, redirect, url_for, Response
from flask.ext.bcrypt import Bcrypt
from flask.ext.gravatar import Gravatar
from flask_wtf.csrf import CsrfProtect
from mongoengine import connect
import json
from datetime import datetime, timedelta

import settings
from models import *
from forms import *


app = Flask(__name__)
app.config.from_object(settings)

bcrypt = Bcrypt(app)
gravatar = Gravatar(app, size=160, default='mm')
csrf = CsrfProtect()

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


@app.route("/event-new/", methods=['GET', 'POST'])
def event_new_page():
    ''' add new event'''
    form = EventForm()
    if request.method == 'POST' and form.validate():
        event_key = form.event_key.data
        title = form.title.data
        available_answers = form.available_answers.data
        available_answers = available_answers.split("\n")
        event = Event(event_key=event_key, title=title, available_answers=available_answers)
        event.dt = datetime.now()
        event.finish_dt = datetime.now() + timedelta(days=7)
        event.close_dt = datetime.now() + timedelta(days=5)
        event.save()
        return redirect(url_for('events_page'))
    else:  # show form
        return render_template('event-new.html', form=form)



@app.route("/event/<event_key>/", methods=['GET', 'POST'])
def event_page(event_key):
    ''' event data '''
    if request.method == 'POST':  # updating prediction
        profile = get_current_profile()
        pe = ProfileEvent()
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


@app.route("/event/<event_key>/edit", methods=[u'GET', 'POST'])
def event_edit_page(event_key):
    ''' event editing'''
    if request.method == 'POST':  # updating prediction
        profile = get_current_profile()
        return redirect(url_for('events_page', event_key=event_key))
    else:  # show forms
        event_key = escape(event_key)
        event = Event.objects(event_key=event_key).first()

        return render_template('event-edit.html', event=event)


@app.route("/api/v1/event/<event_key>/")
def event_api_v1(event_key):
    ''' event data '''
    event_key = escape(event_key)
    event = Event.objects(event_key=event_key).first()
    profile_events = ProfileEvent.objects.filter(event=event_key)
    cntr = Counter()
    for pe in profile_events:
        for a in pe.answers:
            cntr[a] += 1
    answers_stat = [{'name': k, 'value': v} for k,v in dict(cntr).items()]
    return Response(json.dumps(answers_stat, ensure_ascii=False).encode('utf8'),  mimetype='application/json')


if __name__ == "__main__":
    app.run()