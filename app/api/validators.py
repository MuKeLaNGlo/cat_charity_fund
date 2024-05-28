from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject


async def validate_charity_project_name_duplicate(
    project_name: str,
    session: AsyncSession,
) -> None:
    """Проверяется, существует ли такое имя проекта"""
    existing_project = await charity_project_crud.get_project_by_name(
        project_name, session
    )
    if existing_project:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


async def validate_charity_project_exists(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    """Проверяется, существует ли проект с таким id"""
    project = await charity_project_crud.get(project_id, session)
    if not project:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Проект не найден!'
        )
    return project


async def validate_project_before_update(
    project_id: int,
    update_data: dict,
    session: AsyncSession,
) -> CharityProject:
    """
    Валидация перед обновлением проекта.

    Закрытый проект нельзя редактировать.
    Нельзя установить требуемую сумму меньше уже вложенной.
    """
    project = await validate_charity_project_exists(project_id, session)
    if project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!',
        )
    if update_data.get(
        'full_amount'
    ) and project.invested_amount > update_data.get('full_amount'):
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Нельзя установить требуемую сумму меньше уже вложенной!',
        )
    if update_data.get('name') and update_data.get('name') != project.name:
        await validate_charity_project_name_duplicate(
            update_data.get('name'), session
        )
    return project


async def validate_project_before_delete(
    project_id: int, session: AsyncSession
) -> CharityProject:
    """
    Валидация перед удалением проекта.

    Проверка на существование проекта и наличие инвестиций в него.
    """
    project = await validate_charity_project_exists(project_id, session)
    if project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!',
        )
    return project
