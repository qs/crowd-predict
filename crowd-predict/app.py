# coding:utf-8
import os
from authomatic.adapters import WerkzeugAdapter
from cgi import escape
from collections import Counter
from urlparse import urlparse
from flask import Flask, render_template, request, redirect, url_for, Response, make_response
from flask.ext.seasurf import SeaSurf
from flask.ext.bcrypt import Bcrypt
from functools import wraps
from flask.ext.gravatar import Gravatar
from mongoengine import connect
import json
import hashlib

import settings
from models import *
import auth as auth


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

@app.route('/login/<provider_name>/', methods=['GET', 'POST'])
def login(provider_name):
    response = make_response()
    if provider_name != 'email':
        result = auth.authomatic.login(WerkzeugAdapter(request, response), provider_name)
        if result:
            if result.user:
                user = result.user
                prs = Profile.objects.filter(email=user.email)
                if not prs:
                    pr = Profile(**{'email': user.email})
                    pr.save()
            #result.user.update()
            return render_template('login.html', result=result)
        return response
    else:
        pass


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    prf = Profile.objects.get(email=username)
    pwd = hashlib.sha224(password).hexdigest()
    if prf.password == pwd:
        return True
    else:
        return False

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        authoriz = request.authorization
        if not authoriz or not check_auth(authoriz.username, authoriz.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


def get_current_profile():
    result = auth.authomatic.login(Webapp2Adapter(self), 'twitter')
    #profile = Profile.objects(email='acccko@gmail.com').first()
    #return profile


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
    answers_stat = [{'answer': k, 'score': v} for k,v in dict(cntr).items()]
    return Response(json.dumps(answers_stat, ensure_ascii=False).encode('utf8'),  mimetype='application/json')


if __name__ == "__main__":
    app.run()
