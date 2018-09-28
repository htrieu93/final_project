from mongoengine import *

class Vote(Document):
    post_id = StringField()
    user_id = StringField()