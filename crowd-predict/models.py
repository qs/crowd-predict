from mongoengine import Document, StringField, EmailField, DateTimeField, ListField, ReferenceField


class Event(Document):
    event_key = StringField(required=True, primary_key=True)
    title = StringField(required=True)
    available_answers = ListField()
    dt = DateTimeField(required=True)
    close_dt = DateTimeField(required=True)
    finish_dt = DateTimeField(required=True)


class Profile(Document):
    email = EmailField(required=True, primary_key=True)
    dt = DateTimeField(required=True)


class ProfileEvent(Document):
    answer = ListField()
    profile = ReferenceField('Profile', dbref=True)
    event = ReferenceField('Event', dbref=True)
