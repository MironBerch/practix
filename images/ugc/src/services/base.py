from abc import ABC, abstractmethod

from motor.motor_asyncio import AsyncIOMotorDatabase


class BaseService(ABC):
    def __init__(self, mongo: AsyncIOMotorDatabase):
        self.mongo = mongo

    @abstractmethod
    def get(self):
        pass

    @abstractmethod
    def filter(self):
        pass

    @abstractmethod
    def all(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def remove(self):
        pass
