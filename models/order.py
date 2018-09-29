from mongoengine import *

class Order(Document):
    recipe_id = ReferenceField("Recipe")
    user_id = ReferenceField("User")
    time = DateTimeField()
    is_accepted = BooleanField()
    