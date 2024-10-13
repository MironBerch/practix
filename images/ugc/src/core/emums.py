from enum import Enum


class MongoCollections(Enum):
    """Коллекций в MongoDB."""

    users = 'users'
    films = 'films'
    reviews = 'reviews'
