from mongoengine import Document, StringField, DateTimeField
from datetime import datetime


class User(Document):
    name = StringField(required=True, max_length=100)
    email = StringField(required=True, max_length=50, unique=True)
    password = StringField(required=True, max_length=500)
    priv = StringField(required=True, default="low")
    posted = DateTimeField(default=datetime.now())
    meta = {'allow_inheritance': True}
