from fastapi import APIRouter

from api.handlers import router

api_router = APIRouter(prefix='/api')

# Notifications
api_router.include_router(router=router)
