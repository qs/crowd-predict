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
    lst = [{'shden5663@mail.ru':[], },
    {'rom.sheulov@gmail.com': ['REES46', 'schalarm', 'OPPI'], },
    {'fun@mail.ru': ['OPPI', 'schalarm', 'On air'], },
    {'anon1@example.com': ['3D MMM', 'æMind Manipulus', '3D 2Phone', 'GadjetHolder', 'BeHealthier'], },
    {'polinashekleina555@gmail.com': ['BeHealthier', '3D MMM', 'æMind Manipulus', 'GadjetHolder', 'CardiWear'], },
    {'andreypalshin@gmail.com': ['3D MMM', '3D 2Phone', 'æMind Manipulus', 'GadjetHolder', 'BeHealthier'], },
    {'maxigen4@gmail.com': ['3D MMM', '3D 2Phone', 'GadjetHolder', 'CardiWear', 'лагранжиан стандартной модели для чайников'], },
    {'regmail92@mail.ru': ['3D MMM', '3D 2Phone', 'BeHealthier', 'On air', 'GadjetHolder'], },
    {'nikikita@mail.ru': ['æMind Manipulus', 'Биологи', 'Crowd Predicts'], },
    {'soloha_vladimir@hotmail.com': ['schalarm', 'GadjetHolder', 'Crowd Predicts', 'æMind Manipulus'], },
    {'silyakov@gmail.com': ['CardiWear', 'BeHealthier', 'schalarm', 'æMind Manipulus'], },
    {'xakonde@gmail.com': ['æMind Manipulus', 'CardiWear', '3D 2Phone', 'On Air', 'Раскраска котиков'], },
    {'mialerxd@gmail.com': ['æMind Manipulus', 'CardiWear', 'Crowd Predicts'], },
    {'zaharoffv@inbox.ru': ['GadjetHolder', '3D MMM', 'CardiWear', 'æMind Manipulus'], },
    {'yndx.kroniker@yandex.ru': ['On Air', 'GadjetHolder', '3D 2Phone', 'æMind Manipulus'], },
    {'a.aysurarova@gmail.com': ['CardiWear', 'BeHealthier', 'æMind Manipulus'], },
    {'anon2@example.com': ['CardiWear', 'Раскраска котиков', 'æMind Manipulus', 'GadjetHolder', 'On Air'], },
    {'vladimir.diht@yandex.ru': ['æMind Manipulus', 'CardiWear', 'Раскраска котиков'], },
    {'annagrenn@gmail.com': ['æMind Manipulus', 'On Air', 'лагранжиан стандартной модели для чайников'], },
    {'anon3@example.com': ['CardiWear', 'SpectTRIK'], },
    {'anon4@example.com': ['GadjetHolder', 'CardiWear', 'BeHealthier'], },
    {'whoosh.s@gmail.com': ['SunSeat', 'GadjetHolder', 'CardiWear'], },
    {'commonica@yandex.ru': ['CardiWear', '3D 2Phone', 'REES46', 'OPPI', 'On Air'], },
    {'zhur85@gmail.com': ['REES46', 'CardiWear', 'BeHealthier', 'On Air', 'æMind Manipulus'], },
    {'anikarain1991@gmail.com': ['GadjetHolder', 'æMind Manipulus'], },
    {'kotapesik@gmail.com': ['лагранжиан стандартной модели для чайников', 'æMind Manipulus', 'GadjetHolder', 'SpectTRIK', 'CardiWear'], },
    {'acccko@gmail.com': ['CardiWear', 'schalarm', '3D MMM', 'Crowd Predicts', 'лагранжиан стандартной модели для чайников'], },
    {'hnalina@gmail.com': ['GadjetHolder', 'æMind Manipulus', 'CardiWear', 'BeHealthier', 'schalarm'], },]
    for i in lst:
        ep = ProfileEvent()
        ema = i.keys()[0]
        ep.profile = Profile.objects.get(email=ema)
        ep.answers = i[ema]
        ep.event = Event.objects.get(event_key='hackday')
        ep.save()

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