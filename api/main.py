from api.routes import utils

from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(utils.router)
