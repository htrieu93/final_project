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
# recipes = Recipe.objects()

# for recipe in recipes:
#     print(type(recipe.comment_id))

new_recipe = Recipe(
    name = 'QUAN',
    servings = 3,
    comment_id = [],
    instructions = ''
)
new_recipe.save()

# new_comment = Comment(
#     body = 'a'
# )

# new_comment.save()

# new_recipe.update(push__comment_id = new_comment)