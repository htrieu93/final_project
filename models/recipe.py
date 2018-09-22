from mongoengine import *

class Recipe(Document):
    name = StringField()
    servings = IntField()
    image = StringField()
    ingredients = ListField()
    