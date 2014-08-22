# coding:utf-8
import os
from cgi import escape
from urlparse import urlparse
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask.ext.seasurf import SeaSurf
from flask.ext.bcrypt import Bcrypt
from flask.ext.gravatar import Gravatar
from mongoengine import connect

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
    lst = [{'email': 'shden5663@mail.ru'},
    {'email': 'anon1@example.com'},
    {'email': 'anon2@example.com'},
    {'email': 'anon3@example.com'},
    {'email': 'rom.sheulov@gmail.com'},
    {'email': 'fun@mail.ru'},
    {'email': 'polinashekleina555@gmail.com'},
    {'email': 'andreypalshin@gmail.com'},
    {'email': 'maxigen4@gmail.com'},
    {'email': 'regmail92@mail.ru'},
    {'email': 'nikikita@mail.ru'},
    {'email': 'soloha_vladimir@hotmail.com'},
    {'email': 'silyakov@gmail.com'},
    {'email': 'xakonde@gmail.com'},
    {'email': 'mialerxd@gmail.com'},
    {'email': 'zaharoffv@inbox.ru'},
    {'email': 'yndx.kroniker@yandex.ru'},
    {'email': 'a.aysurarova@gmail.com'},
    {'email': 'vladimir.diht@yandex.ru'},
    {'email': 'annagrenn@gmail.com'},
    {'email': 'anon4@example.com'},
    {'email': 'whoosh.s@gmail.com'},
    {'email': 'commonica@yandex.ru'},
    {'email': 'zhur85@gmail.com'},
    {'email': 'anikarain1991@gmail.com'},
    {'email': 'kotapesik@gmail.com'},
    {'email': 'acccko@gmail.com'}, ]
    res = []
    for i in lst:
        p = Profile(**i)
        res.append(p)
    Profile.insert(res)
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
        return render_template('event.html', event=event, profile_events=profile_events)