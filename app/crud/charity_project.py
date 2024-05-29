from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject


class CRUDCharityProject(CRUDBase[CharityProject]):
    async def get_project_by_name(
        self,
        project_name: str,
        session: AsyncSession,
    ) -> Optional[int]:
        charity_project = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        return charity_project.scalars().first()


charity_project_crud = CRUDCharityProject(CharityProject)
