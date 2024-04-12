from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class FavoriteAds(Base):
    __tablename__ = "favorite_ads"
    __mapper_args__ = {"eager_defaults": True}

    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'),
        primary_key=True,

    )
    advertisement_id: Mapped[int] = mapped_column(
        ForeignKey('advertisments.id', ondelete='CASCADE'),
        primary_key=True
    )
