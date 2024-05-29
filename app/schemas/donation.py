from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class DonationBase(BaseModel):
    """Базовая схема для пожертвований."""

    full_amount: int = Field(..., gt=0)
    comment: Optional[str] = None


class DonationCreate(DonationBase):
    """Схема для создания пожертвования."""


class DonationDB(DonationBase):
    """Схема для представления пожертвования."""

    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class AllDonationsDB(DonationDB):
    """Схема для представления всех пожертвований с дополнительными полями."""

    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime] = None
