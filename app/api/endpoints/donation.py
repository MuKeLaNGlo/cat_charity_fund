from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import AllDonationsDB, DonationCreate, DonationDB
from app.services.invest import allocate_funds

router = APIRouter()


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True,
)
async def create_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """Создание нового пожертвования."""
    new_donation = await donation_crud.create(donation, session, user)
    await allocate_funds(session, new_donation)
    return new_donation


@router.get(
    '/',
    response_model=List[AllDonationsDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_donations(session: AsyncSession = Depends(get_async_session)):
    """Просмотр всех донатов, только для суперюзеров."""
    donations = await donation_crud.get_multi(session)
    return donations


@router.get(
    '/my',
    response_model=List[DonationDB],
    response_model_exclude_none=True,
)
async def get_user_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """Получение списка всех донатов текущего пользователя."""
    user_donations = await donation_crud.get_by_user(session, user)
    return user_donations
