from sqlalchemy import Column, ForeignKey, Integer, Text

from app.core.db import Base
from app.models.mixins import DonationMixin


class Donation(DonationMixin, Base):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text, nullable=True)

    def __repr__(self) -> str:
        return f'Пожертвование на сумму {self.total_amount}'
