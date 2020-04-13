# small test, to call: python test.py
# returns printed lines of what's current stored in the database
# as dictionaries. 

from pymongo import MongoClient

client = MongoClient()
db = client.test_database

for post in db.posts.find():
    print(post)