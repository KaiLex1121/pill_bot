from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.enums.advertisment.ad_type import TypeOfAd
from app.enums.advertisment.delivery_type import TypeOfDelivery

from .base import Base
from .drug import Drug


class Advertisment(Base):
    __tablename__ = "advertisments"
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )
    user: Mapped['User'] = relationship('User', back_populates="advertisments")
    drugs: Mapped[list['Drug']] = relationship(back_populates="advertisment")
    ad_type: Mapped[TypeOfAd] = mapped_column(Enum(TypeOfAd))
    delivery_type: Mapped[TypeOfDelivery] = mapped_column(Enum(TypeOfDelivery))
    constant_need: Mapped[bool] = mapped_column()
    city: Mapped[str] = mapped_column()
    additional_text: Mapped[str] = mapped_column()

    def __repr__(self):
        rez = (
            f"<AD "
            f"ID={self.id} "
            f"User={self.user} "
            f"Drugs:{self.drugs}"
        )
        return rez + ">"
