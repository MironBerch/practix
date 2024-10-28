from uuid import UUID

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from db.mongo import get_mongo
from services.base import BaseService


class FilmworksService(BaseService):
    async def get(self, filmwork_id: UUID | str):
        return self.mongo['filmworks'].find_one({'_id': filmwork_id})


def get_filmworks_service(
        mongo: AsyncIOMotorDatabase = Depends(get_mongo),
) -> FilmworksService:
    return FilmworksService(mongo=mongo)
