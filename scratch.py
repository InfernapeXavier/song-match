#  Scratch File to test logic

import datetime
import pymongo
from pymongo import MongoClient


print(pymongo.version)


client = pymongo.MongoClient(
    "mongodb+srv://admin:admin@cluster0-jgksl.mongodb.net/test?retryWrites=true&w=majority")


# Creating new db
db = client.gettingStarted

# creating new collection
people = db.people

# defining document
personDocument = {
    "name": {"first": "Alan", "last": "Turing"},
    "birth": datetime.datetime(1912, 6, 23),
    "death": datetime.datetime(1954, 6, 7),
    "contribs": ["Turing machine", "Turing test", "Turingery"],
    "views": 1250000
}

# inserting document
people.insert_one(personDocument)
