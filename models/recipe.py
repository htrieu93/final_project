from mongoengine import *

class Recipe(Document):
    name = StringField()
    servings = IntField()
    image = StringField()
    ingredients = ListField()
    upvote = IntField(default = 0)
    difficulty = StringField()
    time_of_day = ListField()
    descriptions = StringField()

    