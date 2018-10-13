import mlab
from mongoengine import *

mlab.connect()

class Comment(Document):
    time = DateTimeField()
    body = StringField()

class Recipe(Document):
    # user_id = ListField(ReferenceField(User))
    name = StringField()
    servings = IntField()
    image = StringField()
    ingredients = ListField()
    upvote = IntField(default = 0)
    difficulty = StringField()
    time_of_day = ListField()
    instructions = StringField()
    comment_id = ListField(ReferenceField(Comment))

class User(Document):
    username = StringField()
    password = StringField()
    email = StringField()
    fullname = StringField()
    comment_id = ListField(ReferenceField(Comment))
