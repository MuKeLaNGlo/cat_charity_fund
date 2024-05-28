from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field


class CharityProjectCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: int = Field(..., gt=0)


class CharityProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[int] = Field(None, gt=0)

    class Config:
        extra = Extra.forbid


class CharityProjectDB(BaseModel):
    id: int
    name: str
    description: str
    full_amount: int = Field(..., gt=0)
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime] = None

    class Config:
        orm_mode = True
