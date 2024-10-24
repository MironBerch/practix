from uuid import UUID

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from db.mongo import get_mongo
from services.base import BaseService


class BookmarksService(BaseService):
    async def filter(self, user_id: UUID | str):
        return self.mongo['users'].find({'_id': user_id}).to_list(length=None)

    def update(self, user_id: UUID | str, filmwork_id: UUID | str):
        self.mongo['users'].update_one(
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

    def remove(self, user_id: UUID | str, filmwork_id: UUID | str):
        self.mongo['users'].update_one(
            {'_id': user_id},
            {
                '$pull': {
                    'bookmarks': {
                        'filmwork_id': filmwork_id,
                    }
                }
            },
        )


def get_bookmarks_service(
        mongo: AsyncIOMotorDatabase = Depends(get_mongo),
) -> BookmarksService:
    return BookmarksService(mongo=mongo)
