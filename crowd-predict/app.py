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
    lst = [{'shden5663@mail.ru':[], "_types" : [ "Document", "EventProfile" ], "_cls" : "EventProfile"},
    {'rom.sheulov@gmail.com': [u'REES46', u'schalarm', u'OPPI'], "_types" : [ "Document", "EventProfile" ], "_cls" : "EventProfile"},
    {'fun@mail.ru': [u'OPPI', u'schalarm', u'On air'], "_types" : [ "Document", "EventProfile" ], "_cls" : "EventProfile"},
    {'1': [u'3D MMM', u'æMind Manipulus', u'3D 2Phone', u'GadjetHolder', u'BeHealthier'], "_types" : [ "Document", "EventProfile" ], "_cls" : "EventProfile"},
    {'polinashekleina555@gmail.com': [u'BeHealthier', u'3D MMM', u'æMind Manipulus', u'GadjetHolder', u'CardiWear'], "_types" : [ "Document", "EventProfile" ], "_cls" : "EventProfile"},
    {'andreypalshin@gmail.com': [u'3D MMM', u'3D 2Phone', u'æMind Manipulus', u'GadjetHolder', u'BeHealthier'], "_types" : [ "Document", "EventProfile" ], "_cls" : "EventProfile"},
    {'maxigen4@gmail.com': [u'3D MMM', u'3D 2Phone', u'GadjetHolder', u'CardiWear', u'лагранжиан стандартной модели для чайников'], "_types" : [ "Document", "EventProfile" ], "_cls" : "EventProfile"},
    {'regmail92@mail.ru': [u'3D MMM', u'3D 2Phone', u'BeHealthier', u'On air', u'GadjetHolder'], "_types" : [ "Document", "EventProfile" ], "_cls" : "EventProfile"},
    {'nikikita@mail.ru': [u'æMind Manipulus', u'Биологи', u'Crowd Predicts'], "_types" : [ "Document", "EventProfile" ], "_cls" : "EventProfile"},
    {'soloha_vladimir@hotmail.com': [u'schalarm', u'GadjetHolder', u'Crowd Predicts', u'æMind Manipulus'], "_types" : [ "Document", "EventProfile" ], "_cls" : "EventProfile"},
    {'silyakov@gmail.com': [u'CardiWear', u'BeHealthier', u'schalarm', u'æMind Manipulus'], "_types" : [ "Document", "EventProfile" ], "_cls" : "EventProfile"},
    {'xakonde@gmail.com': [u'æMind Manipulus', u'CardiWear', u'3D 2Phone', u'On Air', u'Раскраска котиков'], "_types" : [ "Document", "EventProfile" ], "_cls" : "EventProfile"},
    {'mialerxd@gmail.com': [u'æMind Manipulus', u'CardiWear', u'Crowd Predicts'], "_types" : [ "Document", "EventProfile" ], "_cls" : "EventProfile"},
    {'zaharoffv@inbox.ru': [u'GadjetHolder', u'3D MMM', u'CardiWear', u'æMind Manipulus'], "_types" : [ "Document", "EventProfile" ], "_cls" : "EventProfile"},
    {'yndx.kroniker@yandex.ru': [u'On Air', u'GadjetHolder', u'3D 2Phone', u'æMind Manipulus'], "_types" : [ "Document", "EventProfile" ], "_cls" : "EventProfile"},
    {'a.aysurarova@gmail.com': [u'CardiWear', u'BeHealthier', u'æMind Manipulus'], "_types" : [ "Document", "EventProfile" ], "_cls" : "EventProfile"},
    {'2': [u'CardiWear', u'Раскраска котиков', u'æMind Manipulus', u'GadjetHolder', u'On Air'], "_types" : [ "Document", "EventProfile" ], "_cls" : "EventProfile"},
    {'vladimir.diht@yandex.ru': [u'æMind Manipulus', u'CardiWear', u'Раскраска котиков'], "_types" : [ "Document", "EventProfile" ], "_cls" : "EventProfile"},
    {'annagrenn@gmail.com': [u'æMind Manipulus', u'On Air', u'лагранжиан стандартной модели для чайников'], "_types" : [ "Document", "EventProfile" ], "_cls" : "EventProfile"},
    {'3': [u'CardiWear', u'SpectTRIK'], "_types" : [ "Document", "EventProfile" ], "_cls" : "EventProfile"},
    {'4': [u'GadjetHolder', u'CardiWear', u'BeHealthier'], "_types" : [ "Document", "EventProfile" ], "_cls" : "EventProfile"},
    {'whoosh.s@gmail.com': [u'SunSeat', u'GadjetHolder', u'CardiWear'], "_types" : [ "Document", "EventProfile" ], "_cls" : "EventProfile"},
    {'commonica@yandex.ru': [u'CardiWear', u'3D 2Phone', u'REES46', u'OPPI', u'On Air'], "_types" : [ "Document", "EventProfile" ], "_cls" : "EventProfile"},
    {'zhur85@gmail.com': [u'REES46', u'CardiWear', u'BeHealthier', u'On Air', u'æMind Manipulus'], "_types" : [ "Document", "EventProfile" ], "_cls" : "EventProfile"},
    {'anikarain1991@gmail.com': [u'GadjetHolder', u'æMind Manipulus'], "_types" : [ "Document", "EventProfile" ], "_cls" : "EventProfile"},
    {'kotapesik@gmail.com': [u'лагранжиан стандартной модели для чайников', u'æMind Manipulus', u'GadjetHolder', u'SpectTRIK', u'CardiWear'], "_types" : [ "Document", "EventProfile" ], "_cls" : "EventProfile"},
    {'acccko@gmail.com': [u'CardiWear', u'schalarm', u'3D MMM', u'Crowd Predicts', u'лагранжиан стандартной модели для чайников'], "_types" : [ "Document", "EventProfile" ], "_cls" : "EventProfile"},]
    for i in lst:
        p = ProfileEvent(**i)
        p.save()
    ProfileEvent.insert(res)


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