from mongoengine import *

class Order(Document):
    service_id = ReferenceField("Service")
    user_id = ReferenceField("User")
    time = DateTimeField()
    is_accepted = BooleanField()
    