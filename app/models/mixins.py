from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, CheckConstraint
from sqlalchemy.ext.declarative import declared_attr


class DonationMixin:
    """Миксин для модели и схемы пожертвования с ограничениями на поля."""

    full_amount = Column(
        Integer,
        CheckConstraint('full_amount > 0', name='full_amount_positive'),
        nullable=False,
    )
    invested_amount = Column(
        Integer,
        CheckConstraint(
            'invested_amount >= 0', name='invested_amount_is_positive'
        ),
        default=0,
    )
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now, nullable=False)
    close_date = Column(DateTime, nullable=True)

    @declared_attr
    def __table_args__(cls):
        return (
            CheckConstraint(
                'invested_amount <= full_amount',
                name='invested_amount_less_than_full_amount',
            ),
        )
