from mongoengine import *

class Comment(Document):
    name = StringField()
    time = DateTimeField()
    comment = StringField()
    memorable = StringField()

    