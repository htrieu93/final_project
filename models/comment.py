from mongoengine import *

class Comment(Document):
    time = DateTimeField()
    body = StringField()

    