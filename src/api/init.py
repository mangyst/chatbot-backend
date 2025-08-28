from fastapi import APIRouter
from .auth import router as auth_router
from .dialogs import router as dialogs_router
from .messages import router as messages_router
from .health import router as health_router

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(dialogs_router)
api_router.include_router(messages_router)
api_router.include_router(health_router)