from mongoengine import *

class Celebrity(Document):
    name = StringField()
    dod = DateTimeField()
    occupation = StringField()
    memorable = StringField()

    