from datetime import datetime
from uuid import UUID

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from api.paginator import Paginator
from db.mongo import get_mongo
from services.base import BaseService
from services.utils import to_binary


class ReviewsService(BaseService):
    async def get(self, user_id: UUID, filmwork_id: UUID):
        result = await self.mongo['reviews'].find_one(
            {'filmwork_id': to_binary(filmwork_id), 'author': to_binary(user_id)},
        )
        return result

    async def filter(self, filmwork_id: UUID, paginator: Paginator):
        result = (
            await self.mongo['reviews']
            .find({'filmwork_id': filmwork_id})
            .skip((paginator.page - 1) * paginator.size)
            .limit(paginator.size)
            .to_list(length=None)
        )
        return result

    async def update(self, user_id: UUID, filmwork_id: UUID, text: str):
        result = await self.mongo['reviews'].update_one(
            {
                'author': to_binary(user_id),
                'filmwork_id': to_binary(filmwork_id),
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

    async def remove(self, user_id: UUID, filmwork_id: UUID):
        result = await self.mongo['reviews'].delete_one(
            {
                'author': to_binary(user_id),
                'filmwork_id': to_binary(filmwork_id),
            }
        )
        return result

    async def get_rating(self, review_id: UUID):
        result = await self.mongo['reviews'].find_one({'_id': to_binary(review_id)})
        return result['rating']

    async def rate(self, review_id: UUID, user_id: UUID, score: int):
        review_filter = {'_id': to_binary(review_id)}
        review: dict = await self.mongo['reviews'].find_one(review_filter)
        votes: list = review.get('rating', {}).get('votes', [])
        for vote in votes:
            if vote['user_id'] == user_id:
                vote['score'] = score
                break
        else:
            votes.append({'user_id': user_id, 'score': score})
        result = await self.mongo['reviews'].update_one(
            {'_id': to_binary(review_id)},
            {'$set': {'rating.votes': votes}},
        )
        return result

    async def unrate(self, review_id: UUID, user_id: UUID):
        result = await self.mongo['reviews'].update_one(
            {'_id': to_binary(review_id)},
            {'$pull': {'rating.votes': {'user_id': user_id}}},
        )
        return result


def get_reviews_service(
        mongo: AsyncIOMotorDatabase = Depends(get_mongo),
) -> ReviewsService:
    return ReviewsService(mongo=mongo)
