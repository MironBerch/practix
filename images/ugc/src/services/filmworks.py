from uuid import UUID

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from db.mongo import get_mongo
from services.base import BaseService


class FilmworksService(BaseService):
    async def get(self, filmwork_id: UUID | str):
        return self.mongo['filmworks'].find_one({'_id': filmwork_id})

    async def get_rating(self, filmwork_id: UUID | str):
        filmwork = await self.mongo['filmworks'].find_one({'_id': filmwork_id})
        return filmwork['rating']

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
        return self.mongo['filmworks'].update_one(
            {'_id': filmwork_id},
            {'$set': {'rating.votes': votes}}
        )

    async def unrate(self, filmwork_id: UUID | str, user_id: UUID | str):
        await self.mongo['filmworks'].update_one(
            {'_id': filmwork_id},
            {
                '$pull': {
                    'rating.votes': {
                        'user_id': user_id,
                    },
                },
            },
        )


def get_filmworks_service(
        mongo: AsyncIOMotorDatabase = Depends(get_mongo),
) -> FilmworksService:
    return FilmworksService(mongo=mongo)
