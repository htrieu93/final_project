from mongoengine import *

class Comment(Document):
    recipe_id = ReferenceField("Recipe")
    name = StringField()
    time = DateTimeField()
    comment = StringField()
    memorable = StringField()

    