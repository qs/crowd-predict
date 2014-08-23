from flask_wtf import Form
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired

class EventForm(Form):
    event_key = StringField('event_key', validators=[DataRequired()])
    title = StringField('title', validators=[DataRequired()])
    available_answers = TextAreaField('available_answers', validators=[DataRequired()])
