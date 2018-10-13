import mlab
from mongoengine import *

mlab.connect()

class Comment(Document):
    time = DateTimeField()
    body = StringField()

class Recipe(Document):
    # user_id = ListField(ReferenceField(User))
    name = StringField(default = '')
    time = IntField(default = 0)
    servings = IntField(default = 0)
    image = StringField(default = '')
    ingredients = ListField(default = [])
    upvote = IntField(default = 0)
    difficulty = StringField(default = '')
    meal_type = StringField(default = [])
    instructions = ListField(default = [])
    comment_id = ListField(ReferenceField(Comment), default = [])

class User(Document):
    username = StringField()
    password = StringField()
    email = StringField()
    fullname = StringField()
    comment_id = ListField(ReferenceField(Comment))
