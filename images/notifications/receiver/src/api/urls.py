from api.handlers import router

from fastapi import APIRouter

api_router = APIRouter(prefix='/api')

# Notifications
api_router.include_router(router=router)
