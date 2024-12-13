from uuid import UUID

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from db.mongo import get_mongo
from services.base import BaseService


class FilmworksService(BaseService):
    async def get(self, filmwork_id: UUID | str):
        result = await self.mongo['filmworks'].find_one({'_id': filmwork_id})
        return result

    async def get_rating(self, filmwork_id: UUID | str):
        result = await self.mongo['filmworks'].find_one({'_id': filmwork_id})
        return result['rating']

    async def rate(
            self,
            filmwork_id: UUID | str,
            user_id: UUID | str,
            score: int | float,
    ):
        filmwork: dict = await self.mongo['filmworks'].find_one(
            {'_id': filmwork_id},
        )
        votes: list = filmwork.get('rating', {}).get('votes', [])
        for vote in votes:
            if vote['user_id'] == user_id:
                vote['score'] = score
                break
        else:
            votes.append({'user_id': user_id, 'score': score})
        result = await self.mongo['filmworks'].update_one(
            {'_id': filmwork_id},
            {'$set': {'rating.votes': votes}}
        )
        return result

    async def unrate(self, filmwork_id: UUID | str, user_id: UUID | str):
        result = await self.mongo['filmworks'].update_one(
            {'_id': filmwork_id},
            {
                '$pull': {
                    'rating.votes': {
                        'user_id': user_id,
                    },
                },
            },
        )
        return result

    def filter(self):
        raise NotImplementedError()

    def update(self):
        raise NotImplementedError()

    def remove(self):
        raise NotImplementedError()


def get_filmworks_service(
        mongo: AsyncIOMotorDatabase = Depends(get_mongo),
) -> FilmworksService:
    return FilmworksService(mongo=mongo)
