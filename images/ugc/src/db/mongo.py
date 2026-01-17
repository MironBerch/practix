from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from core.config import settings


mongo: AsyncIOMotorDatabase


async def start() -> None:
    global mongo
    mongo = AsyncIOMotorDatabase(
        name='ugc_database',
        client=AsyncIOMotorClient(
            host=settings.mongo.host,
            port=settings.mongo.port,
            username=settings.mongo.username,
            password=settings.mongo.password,
            uuidRepresentation='standard',
        ),
    )


async def stop() -> None:
    mongo.client.close()


async def get_mongo() -> AsyncIOMotorDatabase:
    return mongo
