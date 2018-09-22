import mongoengine

#mongodb://<dbuser>:<dbpassword>@ds263832.mlab.com:63832/final_project_c4e20

host = "ds263832.mlab.com"
port = 63832
db_name = "final_project_c4e20"
user_name = "htrieu93"
password = "prototype101"


def connect():
    mongoengine.connect(db_name, host=host, port=port, username=user_name, password=password)
