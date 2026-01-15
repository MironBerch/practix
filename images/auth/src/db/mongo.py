from os import environ

from pymongo import MongoClient

mongo: MongoClient


def start() -> None:
    global mongo
    mongo = MongoClient(
        host=environ.get('MONGO_HOST', 'mongo'),
        port=int(environ.get('MONGO_PORT', 27017)),
        username=environ.get('MONGO_USERNAME', None),
        password=environ.get('MONGO_PASSWORD', None),
        uuidRepresentation='standard',
    )


def stop() -> None:
    mongo.client.close()


def get_mongo() -> MongoClient:
    return mongo
