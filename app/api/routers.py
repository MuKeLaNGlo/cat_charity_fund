from fastapi import APIRouter

from app.api.endpoints import donation_router, project_router, user_router

api_router = APIRouter()
api_router.include_router(
    donation_router, prefix='/donation', tags=['Donations']
)
api_router.include_router(
    project_router, prefix='/charity_project', tags=['Charity Projects']
)
api_router.include_router(user_router)
