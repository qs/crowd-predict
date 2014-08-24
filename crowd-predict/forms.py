from flask_wtf import Form
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired


class EventForm(Form):
    event_key = StringField('event_key')
    title = StringField('title')
    available_answers = TextAreaField('available_answers')
    correct_answers = TextAreaField('correct_answers')

class LoginForm(Form):
    username = StringField('username', validators=[DataRequired()])
    passwd = StringField('passwd', validators=[DataRequired()])
