import os
from datetime import datetime
from urlparse import urlparse
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flaskext.seasurf import SeaSurf
from flaskext.bcrypt import Bcrypt
from flaskext.gravatar import Gravatar
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

class User(Document):
	username = StringField(required=True)
	email = EmailField(required=True)
	first_name = StringField(max_length=50)
	last_name = StringField(max_length=50)
	location = StringField()
	homepage = StringField()
	passhash = StringField()
	created = DateTimeField()

	meta = {
        'ordering': ['-created']
    }

class Job(Document):
	company_name = StringField(required=True)
	company_location = StringField(required=True)
	company_url = URLField(required=True)
	job_title = StringField(required=True)
	job_posting = StringField(required=True)
	application_instructions = StringField(required=True)
	created = DateTimeField()

	meta = {
        'ordering': ['-created']
    }

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("logged_in"):
        	return f(*args, **kwargs)
        else:
			flash(u'Login is required.', 'warning')
			return redirect(url_for('login', next=request.url))
    return decorated_function

@app.template_filter()
def timesince(dt, default="just now"):
    """
    Returns string representing "time since" e.g.
    3 days ago, 5 hours ago etc.
    """

    now = datetime.utcnow()
    diff = now - dt
    
    periods = (
        (diff.days / 365, "year", "years"),
        (diff.days / 30, "month", "months"),
        (diff.days / 7, "week", "weeks"),
        (diff.days, "day", "days"),
        (diff.seconds / 3600, "hour", "hours"),
        (diff.seconds / 60, "minute", "minutes"),
        (diff.seconds, "second", "seconds"),
    )

    for period, singular, plural in periods:
        
        if period:
            return "%d %s ago" % (period, singular if period == 1 else plural)

    return default

@app.route("/")
def home():
	jobs = Job.objects.all()
	return render_template('home.html', jobs=jobs)

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/contact')
def contact():
	return render_template('contact.html')

@app.route('/create', methods=['GET', 'POST'])
@login_required
def create_job():
	if request.method == 'POST':
		job = Job(company_name=request.form['company_name'])
		job.company_location=request.form['company_location']
		company_url=request.form['company_url']
		if company_url[:4] == 'http':
			job.company_url=company_url
		else:
			job.company_url='http://'+company_url
		job.job_title=request.form['job_title']
		job.job_posting=request.form['job_posting']
		job.application_instructions=request.form['application_instructions']
		job.created=datetime.utcnow()
		job.save()
		next_url = job.id
		flash(u'Job successfully created.', 'success')
		return redirect(url_for('show_job', job_id=next_url))
	else:
		return render_template('create_job.html')

@app.route('/signup', methods=['GET', 'POST'])
def signin():
	if request.method == 'POST':
		if request.form['password'] == request.form['password2']:
			user = User(username=request.form['username'])
			user.email=request.form['email']
			user.first_name=request.form['first_name']
			user.last_name=request.form['last_name']
			user.location='None'
			user.passhash=bcrypt.generate_password_hash(request.form['password'])
			user.homepage='None'
			user.created=datetime.utcnow()
			user.save()
			user_id=user.id
			session['username'] = user.username
			session['logged_in'] = True
			flash(u'Successfully created new user.', 'success')
			return redirect(url_for('show_user', user_id=user_id))
		else:
			flash(u'Passwords do not match.', 'error')
			return render_template('create_user.html')
	else:
		return render_template('create_user.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	next = request.values.get('next', '')
	if request.method == 'POST':
		try:
			user = User.objects.get(username=request.form['username'])
		except User.DoesNotExist:
			flash(u'Password or Username is incorrect.', 'error')
			return render_template('login.html')
		else:
		 	if not bcrypt.check_password_hash(user.passhash, request.form['password']):
				flash(u'Password or Username is incorrect.', 'error')
				return render_template('login.html')
			else:
				session['username'] = user.username
				session['logged_in'] = True
				flash(u'You have been successfully logged in.', 'success')
				return redirect(next or url_for('home'))
	return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('logged_in', None)
    flash(u'You have been successfully logged out.', 'info')
    return redirect(url_for('home'))

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
	if request.method == 'POST':
		user=User.objects.get(username=session.get('username'))
		user.email=request.form['email']
		user.first_name=request.form['first_name']
		user.last_name=request.form['last_name']
		user.location=request.form['location']
		user.homepage=request.form['homepage']
		user.save()
		user_id=user.id
		flash(u'Profile was successfully updated.', 'success')
		return redirect(url_for('show_user', user_id=user_id))
	else:
		user=User.objects.get(username=session.get('username'))
		return render_template('settings.html', user=user)


@app.route('/user/<user_id>')
def show_user(user_id):
	user = User.objects.with_id(user_id)
	return render_template('show_user.html', user=user)

@app.route('/job/<job_id>')
def show_job(job_id):
	job = Job.objects.with_id(job_id)
	return render_template('show_job.html', job=job)

@app.route('/users')
def show_all_users():
	users = User.objects.all()
	return render_template('show_all_users.html', users=users)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.debug = True
    app.run(host='0.0.0.0', port=port)