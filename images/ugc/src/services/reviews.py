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

    async def get_rating(self, review_id):
        review = await self.mongo['reviews'].find_one({'_id': review_id})
        return review['rating']

    async def rate(self, review_id, user_id, score):
        review_filter = {'_id': review_id}
        review: dict = await self.mongo['reviews'].find_one(review_filter)
        votes: list = review.get('rating', {}).get('votes', [])
        for vote in votes:
            if vote['user_id'] == user_id:
                vote['score'] = score
                break
        else:
            votes.append({'user_id': user_id, 'score': score})
        return self.mongo['reviews'].update_one(
            {'_id': review_id},
            {'$set': {'rating.votes': votes}},
        )

    async def unrate(self, review_id, user_id):
        await self.mongo['reviews'].update_one(
            {'_id': review_id},
            {'$pull': {'rating.votes': {'user_id': user_id}}},
        )


def get_reviews_service(
        mongo: AsyncIOMotorDatabase = Depends(get_mongo),
) -> ReviewsService:
    return ReviewsService(mongo=mongo)
