from datetime import datetime
from typing import Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import false

from app.models import CharityProject, Donation


async def allocate_funds(
    session: AsyncSession, entity: Union[Donation, CharityProject]
) -> Union[Donation, CharityProject]:
    """Функция для пожертвований проекту."""
    model_to_use = CharityProject if isinstance(entity, Donation) else Donation

    result = await session.execute(
        select(model_to_use).where(model_to_use.fully_invested == false())
    )
    entities_to_fund = result.scalars().all()

    remaining_funds = entity.full_amount - entity.invested_amount

    for funding_entity in entities_to_fund:
        if remaining_funds <= 0:
            break

        required_funds = (
            funding_entity.full_amount - funding_entity.invested_amount
        )
        allocation = min(remaining_funds, required_funds)

        funding_entity.invested_amount += allocation
        entity.invested_amount += allocation
        remaining_funds -= allocation

        if funding_entity.invested_amount == funding_entity.full_amount:
            funding_entity.fully_invested = True
            funding_entity.close_date = datetime.now()

        if entity.invested_amount == entity.full_amount:
            entity.fully_invested = True
            entity.close_date = datetime.now()

    await session.commit()
    await session.refresh(entity)
    return entity
