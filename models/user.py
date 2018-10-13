from mongoengine import *

class Comment(Document):
    time = DateTimeField()
    body = StringField()

class User(Document):
    username = StringField()
    password = StringField()
    email = StringField()
    fullname = StringField()
    comment_id = ListField(ReferenceField(Comment))
    