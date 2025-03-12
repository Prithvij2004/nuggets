from api.routes import utils, users, notes

from fastapi import APIRouter

api_router = APIRouter()

api_router.include_router(utils.router)
api_router.include_router(users.router)
api_router.include_router(notes.router)
