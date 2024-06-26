from sqlalchemy import BigInteger
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.models import dto
from app.models.database.base import Base


class User(Base):
    __tablename__ = "users"
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    first_name: Mapped[str]
    last_name: Mapped[str | None]
    username: Mapped[str | None]
    is_bot: Mapped[bool] = mapped_column(default=False)
    is_banned: Mapped[bool] = mapped_column(default=False)
    is_admin: Mapped[bool] = mapped_column(default=False)
    language_code: Mapped[str | None] = mapped_column(default=None)
    advertisments: Mapped[list['Advertisment'] | None] = relationship(
        back_populates="user",
        lazy="selectin"
    )
    favorite_advertisements: Mapped[list['Advertisment']] = relationship(
        secondary='favorite_ads',
        back_populates='favorited_by',
        lazy="selectin"
    )

    def to_dto(self) -> dto.User:
        return dto.User(
            db_id=self.id,
            tg_id=self.tg_id,
            first_name=self.first_name,
            last_name=self.last_name,
            username=self.username,
            is_bot=self.is_bot,
            language_code=self.language_code,
            is_admin=self.is_admin,
            is_banned=self.is_banned
        )

    def __repr__(self):
        rez = (
            f"<User "
            f"ID={self.tg_id} "
            f"name={self.first_name} {self.last_name} "
        )
        if self.username:
            rez += f"username=@{self.username}"
        return rez + ">"
