from app.dao.base import BaseDAO
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.database import Advertisment
from app.enums.advertisment import TypeOfDelivery, TypeOfAd
from sqlalchemy.future import select
from sqlalchemy import and_, desc, func


class AdvertismentDAO(BaseDAO[Advertisment]):
    def __init__(self, session: AsyncSession):
        super().__init__(Advertisment, session)

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
        result = await self.session.execute(
            select(self.model)
            .where(*conditions)
            .order_by(desc(self.model.created_at))
            .offset(offset_)
            .limit(limit_)
        )
        profile = result.scalars().first()
        return profile

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