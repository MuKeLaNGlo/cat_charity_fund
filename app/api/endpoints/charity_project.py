from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    validate_charity_project_name_duplicate,
    validate_project_before_delete,
    validate_project_before_update,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)
from app.services.invest import allocate_funds

router = APIRouter()


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True,
    summary='Получить список всех проектов',
)
async def get_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    """Получить список всех проектов."""
    return await charity_project_crud.get_multi(session)


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
    summary='Создание проекта, только суперюзером',
)
async def create_charity_project(
    project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Создание проекта, только суперюзером."""
    await validate_charity_project_name_duplicate(project.name, session)
    new_project = await charity_project_crud.create(project, session)
    new_project = await allocate_funds(session, new_project)
    return new_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
    summary='Редактирование проектов, для суперюзеров',
)
async def update_charity_project(
    project_id: int,
    update_data: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперюзеров.

    Закрытый проект нельзя редактировать.
    Нельзя установить требуемую сумму меньше уже вложенной.
    """
    project = await validate_project_before_update(
        project_id, update_data.dict(), session
    )
    project = await charity_project_crud.update(project, update_data, session)
    return project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
    summary='Удаление проекта',
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Удаление проекта."""
    project = await validate_project_before_delete(project_id, session)
    project = await charity_project_crud.remove(project, session)
    return project
