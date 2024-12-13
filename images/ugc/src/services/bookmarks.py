from uuid import UUID

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from api.paginator import Paginator
from db.mongo import get_mongo
from services.base import BaseService


class BookmarksService(BaseService):
    async def filter(self, user_id: UUID | str, paginator: Paginator):
        result = (
            await self.mongo['users']
            .find({'_id': user_id})
            .skip((paginator.page - 1) * paginator.size)
            .limit(paginator.size)
            .to_list(length=None)
        )
        return result

    async def update(self, user_id: UUID | str, filmwork_id: UUID | str):
        result = await self.mongo['users'].update_one(
            {'_id': user_id},
            {
                '$addToSet': {
                    'bookmarks': {
                        'filmwork_id': filmwork_id,
                    }
                }
            },
            upsert=True,
        )
        return result

    async def remove(self, user_id: UUID | str, filmwork_id: UUID | str):
        result = await self.mongo['users'].update_one(
            {'_id': user_id},
            {
                '$pull': {
                    'bookmarks': {
                        'filmwork_id': filmwork_id,
                    }
                }
            },
        )
        return result

    def get(self):
        raise NotImplementedError()

    def get_rating(self):
        raise NotImplementedError()

    def rate(self):
        raise NotImplementedError()

    def unrate(self):
        raise NotImplementedError()


def get_bookmarks_service(
        mongo: AsyncIOMotorDatabase = Depends(get_mongo),
) -> BookmarksService:
    return BookmarksService(mongo=mongo)
