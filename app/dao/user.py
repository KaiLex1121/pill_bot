from typing import Literal
import datetime

from sqlalchemy import and_, func, update
from sqlalchemy.future import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.base import BaseDAO
from app.models.database import User, Advertisment
from app.models import dto


class UserDAO(BaseDAO[User]):

    def __init__(self, session: AsyncSession):
        super().__init__(User, session)

    async def get_all_user_ads_by_id(self, db_id) -> list[Advertisment]:
        user = await self.get_by_id(db_id)
        return user.advertisments

    async def get_by_tg_id(self, tg_id: int) -> User:
        result = await self.session.execute(
            select(User)
            .where(User.tg_id == tg_id)
        )

        return result.unique().scalar()

    async def ban_user_by_username(self, username):
        await self.session.execute(
            update(self.model)
            .where(self.model.username == username)
            .values(is_banned=True)
        )
        await self.commit()

    async def unban_user_by_username(self, username):
        await self.session.execute(
            update(self.model)
            .where(self.model.username == username)
            .values(is_banned=False)
        )
        await self.commit()

    async def ban_user_by_db_id(self, db_id):
        await self.session.execute(
            update(self.model)
            .where(self.model.id == db_id)
            .values(is_banned=True)
        )
        await self.commit()

    async def unban_user_by_db_id(self, db_id):
        await self.session.execute(
            update(self.model)
            .where(self.model.id == db_id)
            .values(is_banned=False)
        )
        await self.commit()

    async def get_required_users_count_for_required_day(
        self,
        required_type: Literal['new_users', 'active_users'],
        days_ago: int = 0
    ) -> int:
        required_date = datetime.date.today() - datetime.timedelta(days_ago)
        required_date_start = datetime.datetime(
            required_date.year,
            required_date.month,
            required_date.day
        )
        required_date_end = datetime.datetime(
            required_date.year,
            required_date.month,
            required_date.day,
            23, 59, 59
        )
        if required_type == 'new_users':
            required_field = self.model.created_at
        elif required_type == "active_users":
            required_field = self.model.updated_at
        result = await self.session.execute(
            select(func.count(self.model.id))
            .where(
                and_(
                    required_field >= required_date_start,
                    required_field <= required_date_end
                )
            )
        )
        return result.scalar_one()

    async def get_for_seven_days(self) -> list[User]:

        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)

        result = await self.session.execute(
            select(func.count(self.model.id))
            .where(
                and_(
                    self.model.created_at >= start_date,
                    self.model.created_at <= end_date
                )
            )
        )
        return result.scalar_one()

    async def upsert_user(self, user: dto.User) -> dto.User:
        kwargs = dict(
            tg_id=user.tg_id,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            is_bot=user.is_bot,
            language_code=user.language_code,
            updated_at=func.now(),
        )

        saved_user = await self.session.execute(
            insert(User)
            .values(**kwargs)
            .on_conflict_do_update(
                index_elements=(User.tg_id,),
                set_=dict(**kwargs),
                where=User.tg_id == user.tg_id,
            )
            .returning(User)
        )
        return saved_user.scalar_one().to_dto()
