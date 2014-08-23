from mongoengine import Document, StringField, EmailField, DateTimeField, ListField, ReferenceField, IntField


class Event(Document):
    event_key = StringField(required=True, primary_key=True)
    title = StringField(required=True)
    available_answers = ListField()
    dt = DateTimeField(required=True)
    close_dt = DateTimeField(required=True)
    finish_dt = DateTimeField(required=True)
    author = ReferenceField('Profile', dbref=True)
    correct_answers = ListField()
    answers_max = IntField(required=True, default=5)


class Profile(Document):
    email = EmailField(required=True, primary_key=True)
    password = StringField(required=False)
    dt = DateTimeField()


class ProfileEvent(Document):
    answers = ListField()
    profile = ReferenceField('Profile', dbref=True)
    event = ReferenceField('Event', dbref=True)
    dt = DateTimeField(required=True)
