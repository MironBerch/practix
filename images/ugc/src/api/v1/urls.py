from fastapi import APIRouter

from src.api.v1.handlers import bookmarks

api_v1_router = APIRouter(prefix='/v1')

api_v1_router.include_router(router=bookmarks.router)
