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
    lst = [{'email': 'shden5663@mail.ru', "_types" : [ "Document", "Profile" ], "_cls" : "Profile"},
    {'email': 'anon1@example.com', "_types" : [ "Document", "Profile" ], "_cls" : "Profile"},
    {'email': 'anon2@example.com', "_types" : [ "Document", "Profile" ], "_cls" : "Profile"},
    {'email': 'anon3@example.com', "_types" : [ "Document", "Profile" ], "_cls" : "Profile"},
    {'email': 'rom.sheulov@gmail.com', "_types" : [ "Document", "Profile" ], "_cls" : "Profile"},
    {'email': 'fun@mail.ru', "_types" : [ "Document", "Profile" ], "_cls" : "Profile"},
    {'email': 'polinashekleina555@gmail.com', "_types" : [ "Document", "Profile" ], "_cls" : "Profile"},
    {'email': 'andreypalshin@gmail.com', "_types" : [ "Document", "Profile" ], "_cls" : "Profile"},
    {'email': 'maxigen4@gmail.com', "_types" : [ "Document", "Profile" ], "_cls" : "Profile"},
    {'email': 'regmail92@mail.ru', "_types" : [ "Document", "Profile" ], "_cls" : "Profile"},
    {'email': 'nikikita@mail.ru', "_types" : [ "Document", "Profile" ], "_cls" : "Profile"},
    {'email': 'soloha_vladimir@hotmail.com', "_types" : [ "Document", "Profile" ], "_cls" : "Profile"},
    {'email': 'silyakov@gmail.com', "_types" : [ "Document", "Profile" ], "_cls" : "Profile"},
    {'email': 'xakonde@gmail.com', "_types" : [ "Document", "Profile" ], "_cls" : "Profile"},
    {'email': 'mialerxd@gmail.com', "_types" : [ "Document", "Profile" ], "_cls" : "Profile"},
    {'email': 'zaharoffv@inbox.ru', "_types" : [ "Document", "Profile" ], "_cls" : "Profile"},
    {'email': 'yndx.kroniker@yandex.ru', "_types" : [ "Document", "Profile" ], "_cls" : "Profile"},
    {'email': 'a.aysurarova@gmail.com', "_types" : [ "Document", "Profile" ], "_cls" : "Profile"},
    {'email': 'vladimir.diht@yandex.ru', "_types" : [ "Document", "Profile" ], "_cls" : "Profile"},
    {'email': 'annagrenn@gmail.com', "_types" : [ "Document", "Profile" ], "_cls" : "Profile"},
    {'email': 'anon4@example.com', "_types" : [ "Document", "Profile" ], "_cls" : "Profile"},
    {'email': 'whoosh.s@gmail.com', "_types" : [ "Document", "Profile" ], "_cls" : "Profile"},
    {'email': 'commonica@yandex.ru', "_types" : [ "Document", "Profile" ], "_cls" : "Profile"},
    {'email': 'zhur85@gmail.com', "_types" : [ "Document", "Profile" ], "_cls" : "Profile"},
    {'email': 'anikarain1991@gmail.com', "_types" : [ "Document", "Profile" ], "_cls" : "Profile"},
    {'email': 'kotapesik@gmail.com', "_types" : [ "Document", "Profile" ], "_cls" : "Profile"},
    {'email': 'acccko@gmail.com', "_types" : [ "Document", "Profile" ], "_cls" : "Profile"},
    {'email': 'hnalina@gmail.com', "_types" : [ "Document", "Profile" ], "_cls" : "Profile"},]
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