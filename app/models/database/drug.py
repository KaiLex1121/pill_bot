from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from .base import Base


class Drug(Base):
    __tablename__ = "drugs"
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[int] = mapped_column(primary_key=True)
    ad_id: Mapped[int] = mapped_column(
        ForeignKey("advertisments.id", ondelete="CASCADE")
    )
    advertisment: Mapped['Advertisment'] = relationship(back_populates='drugs')
    name: Mapped[str] = mapped_column()

    def __repr__(self):
        rez = (
            f"<Drug"
            f"ID={self.id} "
            f"Name={self.name}"
            f"AD={self.advertisment} "
        )
        return rez + ">"
