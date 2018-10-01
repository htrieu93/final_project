from mongoengine import *

class Comment(Document):
    recipe_id = ReferenceField("Recipe")
    user_id = ReferenceField("User")
    time = DateTimeField()
    time = DateTimeField()
    comment = StringField()
    memorable = StringField()

    