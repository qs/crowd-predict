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
    lst = [{'shden5663@mail.ru':[]},
    {'rom.sheulov@gmail.com': [u'REES46', u'schalarm', u'OPPI']},
    {'fun@mail.ru': [u'OPPI', u'schalarm', u'On air']},
    {'1': [u'3D MMM', u'æMind Manipulus', u'3D 2Phone', u'GadjetHolder', u'BeHealthier']},
    {'polinashekleina555@gmail.com': [u'BeHealthier', u'3D MMM', u'æMind Manipulus', u'GadjetHolder', u'CardiWear']},
    {'andreypalshin@gmail.com': [u'3D MMM', u'3D 2Phone', u'æMind Manipulus', u'GadjetHolder', u'BeHealthier']},
    {'maxigen4@gmail.com': [u'3D MMM', u'3D 2Phone', u'GadjetHolder', u'CardiWear', u'лагранжиан стандартной модели для чайников']},
    {'regmail92@mail.ru': [u'3D MMM', u'3D 2Phone', u'BeHealthier', u'On air', u'GadjetHolder']},
    {'nikikita@mail.ru': [u'æMind Manipulus', u'Биологи', u'Crowd Predicts']},
    {'soloha_vladimir@hotmail.com': [u'schalarm', u'GadjetHolder', u'Crowd Predicts', u'æMind Manipulus']},
    {'silyakov@gmail.com': [u'CardiWear', u'BeHealthier', u'schalarm', u'æMind Manipulus']},
    {'xakonde@gmail.com': [u'æMind Manipulus', u'CardiWear', u'3D 2Phone', u'On Air', u'Раскраска котиков']},
    {'mialerxd@gmail.com': [u'æMind Manipulus', u'CardiWear', u'Crowd Predicts']},
    {'zaharoffv@inbox.ru': [u'GadjetHolder', u'3D MMM', u'CardiWear', u'æMind Manipulus']},
    {'yndx.kroniker@yandex.ru': [u'On Air', u'GadjetHolder', u'3D 2Phone', u'æMind Manipulus']},
    {'a.aysurarova@gmail.com': [u'CardiWear', u'BeHealthier', u'æMind Manipulus']},
    {'2': [u'CardiWear', u'Раскраска котиков', u'æMind Manipulus', u'GadjetHolder', u'On Air']},
    {'vladimir.diht@yandex.ru': [u'æMind Manipulus', u'CardiWear', u'Раскраска котиков']},
    {'annagrenn@gmail.com': [u'æMind Manipulus', u'On Air', u'лагранжиан стандартной модели для чайников']},
    {'3': [u'CardiWear', u'SpectTRIK']},
    {'4': [u'GadjetHolder', u'CardiWear', u'BeHealthier']},
    {'whoosh.s@gmail.com': [u'SunSeat', u'GadjetHolder', u'CardiWear']},
    {'commonica@yandex.ru': [u'CardiWear', u'3D 2Phone', u'REES46', u'OPPI', u'On Air']},
    {'zhur85@gmail.com': [u'REES46', u'CardiWear', u'BeHealthier', u'On Air', u'æMind Manipulus']},
    {'anikarain1991@gmail.com': [u'GadjetHolder', u'æMind Manipulus']},
    {'kotapesik@gmail.com': [u'лагранжиан стандартной модели для чайников', u'æMind Manipulus', u'GadjetHolder', u'SpectTRIK', u'CardiWear']},
    {'acccko@gmail.com': [u'CardiWear', u'schalarm', u'3D MMM', u'Crowd Predicts', u'лагранжиан стандартной модели для чайников']},]
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