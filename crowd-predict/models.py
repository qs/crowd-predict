from mongoengine import Document, StringField, EmailField, DateTimeField, URLField


class Event(Document):
    title = StringField(required=True)
    dt = DateTimeField(required=True)
    close_dt = DateTimeField(required=True)
    finish_dt = DateTimeField(required=True)

    meta = {
        'ordering': ['-dt']
    }
