from datetime import datetime
from uuid import UUID

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from api.paginator import Paginator
from db.mongo import get_mongo
from services.base import BaseService


class ReviewsService(BaseService):
    async def get(self, user_id: UUID | str, filmwork_id: UUID | str):
        return self.mongo['reviews'].find_one(
            {'filmwork_id': filmwork_id, 'author': user_id},
        )

    async def filter(self, filmwork_id: UUID | str, paginator: Paginator):
        return (
            self.mongo['reviews']
            .find({'filmwork_id': filmwork_id})
            .skip((paginator.page - 1) * paginator.size)
            .limit(paginator.size)
            .to_list(length=None)
        )

    async def update(self, user_id: UUID | str, filmwork_id: UUID | str, text: str):
        result = await self.mongo['reviews'].update_one(
            {
                'author': user_id,
                'filmwork_id': filmwork_id,
            },
            {
                '$set': {
                    'text': text,
                    'pub_date': datetime.now(),
                },
                '$setOnInsert': {
                    'text': text,
                }
            },
            upsert=True,
        )
        return result

    async def remove(self, user_id: UUID | str, filmwork_id: UUID | str):
        result = await self.mongo['reviews'].delete_one(
            {
                'author': user_id,
                'filmwork_id': filmwork_id,
            }
        )
        return result


def get_reviews_service(
        mongo: AsyncIOMotorDatabase = Depends(get_mongo),
) -> ReviewsService:
    return ReviewsService(mongo=mongo)
