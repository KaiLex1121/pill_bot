from app.dao.base import BaseDAO
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.database import Advertisment
from app.enums.advertisment import TypeOfDelivery, TypeOfAd
from sqlalchemy.future import select
from sqlalchemy import and_, desc, func, update


class AdvertismentDAO(BaseDAO[Advertisment]):
    def __init__(self, session: AsyncSession):
        super().__init__(Advertisment, session)

    async def hide_ad_by_id(self, ad_id):
        await self.session.execute(
            update(self.model)
            .where(self.model.id == ad_id)
            .values(is_hidden=True)
        )
        await self.commit()

    async def unhide_ad_by_id(self, ad_id):
        await self.session.execute(
            update(self.model)
            .where(self.model.id == ad_id)
            .values(is_hidden=False)
        )
        await self.commit()

    async def get_required_ads_by_limit(
        self,
        ad_type: str,
        drugs: str,
        city: str,
        offset_: int,
        limit_: int,
    ) -> Advertisment:
        conditions = []
        if ad_type != 'all_ad_types':
            conditions.append(self.model.ad_type == TypeOfAd[ad_type])
        conditions.append(self.model.city.ilike(f"%{city}%"))
        conditions.append(self.model.drugs.ilike(f"%{drugs}%"))
        conditions.append(self.model.is_hidden == False)
        result = await self.session.execute(
            select(self.model)
            .where(*conditions)
            .order_by(desc(self.model.created_at))
            .offset(offset_)
            .limit(limit_)
        )
        ad = result.scalars().first()
        return ad

    async def create_ad(self, user_id, FSM_dict: dict):
        new_ad = Advertisment(
            user_id=user_id,
            ad_type=TypeOfAd[FSM_dict['ad_type']],
            city=FSM_dict['city'],
            drugs=FSM_dict['drugs'],
            delivery_type=TypeOfDelivery[FSM_dict['delivery_type']],
            additional_text=FSM_dict['additional_text'],
        )
        self.save(new_ad)
        await self.session.commit()