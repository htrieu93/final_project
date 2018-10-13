from pymongo import MongoClient, DESCENDING
import cloudinary
from cloudinary import uploader
import os

#Config cloudinary cloud
cloudinary.config(
  cloud_name = 'flask-image',  
  api_key = '133444264233997',  
  api_secret = 'SrlSO-4T4W2lQx72PEYGHSEnOwU'
)

#Path of current file
my_path = os.path.abspath(os.path.dirname(__file__))


def convert_local_to_url(uri, collection, url_field):
    client = MongoClient(uri)
    db_name = uri.split("/")[-1]
    db = client[db_name]
    docs = db[collection].find({})
    for doc in docs:
        #Upload file to free host
        try:
          if doc[url_field] == '':
            continue
          else:
            path = os.path.join(my_path, doc[url_field])
            image_file = open(path, 'rb')
            imager = uploader.upload(image_file)
            link = imager['url']
            #return new url to db
            doc[url_field] = link
            db[collection].update_one({'_id':doc['_id']}, {"$set": doc}, upsert=False)
        except KeyError:
          continue
        except OSError:
          continue

convert_local_to_url("mongodb://htrieu:prototype101@ds263832.mlab.com:63832/final_project_c4e20", "recipe", "image")