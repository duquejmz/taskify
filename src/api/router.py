from fastapi import APIRouter

from src.api.routes import auth, task, user, tag, permission, role


api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(task.router)
api_router.include_router(user.router)
api_router.include_router(tag.router)
api_router.include_router(permission.router)
api_router.include_router(role.router)
