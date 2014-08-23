# coding:utf-8
import os
from authomatic.adapters import WerkzeugAdapter
from cgi import escape
from collections import Counter
from urlparse import urlparse
from flask import Flask, render_template, request, redirect, url_for, Response, make_response, session
from flask.ext.seasurf import SeaSurf
from flask.ext.bcrypt import Bcrypt
from functools import wraps
from flask.ext.gravatar import Gravatar
from flask_wtf.csrf import CsrfProtect
from mongoengine import connect
import json
import hashlib

import settings
from models import *
from forms import *
import auth as auth
from datetime import datetime, timedelta


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


@app.route('/login/<provider_name>/', methods=['GET', 'POST'])
def login(provider_name):
    form = LoginForm()
    response = make_response()
    if provider_name == 'form':
        result = None
        context = dict(result=result, session=session, form=form)
        return render_template('login.html', **context)
    elif provider_name != 'email':
        result = auth.authomatic.login(WerkzeugAdapter(request, response), provider_name)
        if result:
            if result.user:
                user = result.user
                session['username'] = user.email
                prs = Profile.objects.filter(email=user.email)
                if not prs:
                    pr = Profile(**{'email': user.email})
                    pr.save()
            return render_template('login.html', result=result, session=session)
        return response
    else:
        prf = Profile.objects.filter(email=form.username.data)
        print 'prf get, %s' % form.username.data
        prfs = Profile.objects.all()
        for i in prfs:
            print i.email
        if not prf:
            print 'not prf, redirect'
            try:
                redirect(url_for('login', provider_name='form'))
            except Exception, e:
                print e
        else:
            print 'prf check'
            if check_auth(form.username.data, form.passwd.data):
                print 'checked'
                redirect(url_for('home_page'))


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    prf = Profile.objects.get(email=username)
    session['username'] = prf.email
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
    profile = Profile.objects(email='acccko@gmail.com').first()
    session['username'] = profile.email
    return profile


@app.route("/")
def home_page():
    ''' redirects to event page '''
    return redirect(url_for('events_page'))


@app.route("/events/")
def events_page():
    ''' list of events '''
    try:
        events = Event.objects.all()
        res = render_template('events.html', events=events, session=session)
    except Exception,e :
        print e
    return render_template('events.html', events=events, session=session)


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
        return render_template('event-new.html', form=form, session=session)


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

        return render_template('event.html', event=event, profile_events=profile_events, session=session)


@app.route("/event/<event_key>/edit", methods=[u'GET', 'POST'])
def event_edit_page(event_key):
    ''' event editing'''
    if request.method == 'POST':  # updating prediction
        profile = get_current_profile()
        return redirect(url_for('events_page', event_key=event_key))
    else:  # show forms
        event_key = escape(event_key)
        event = Event.objects(event_key=event_key).first()

        return render_template('event-edit.html', event=event, session=session)


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
