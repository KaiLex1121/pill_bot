from app.dao.base import BaseDAO
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.database import Advertisment
from app.enums.advertisment import TypeOfDelivery, TypeOfAd
from sqlalchemy.future import select
from sqlalchemy import and_, func


class AdvertismentDAO(BaseDAO[Advertisment]):
    def __init__(self, session: AsyncSession):
        super().__init__(Advertisment, session)

    async def get_required_ads_by_limit(
        self,
        drugs: str,
        city: str,
        offset_: int,
        limit_: int,

    ) -> Advertisment:
        result = await self.session.execute(
            select(self.model)
            .where(
                and_(
                    self.model.ad_type == "give",
                    self.model.city.like(f"%{city}%"),
                    self.model.drugs.like(f"%{drugs}%")
                )
            )
            .offset(offset_)
            .limit(limit_)
        )
        profile = result.scalars().first()
        return profile

    async def create_ad(self, user_id, FSM_dict: dict):
        new_ad = Advertisment(
            user_id=user_id,
            ad_type=TypeOfAd(FSM_dict['ad_type']),
            city=FSM_dict['city'],
            drugs=FSM_dict['drugs'],
            delivery_type=TypeOfDelivery(FSM_dict['delivery_type']),
            additional_text=FSM_dict['additional_text'],
        )
        self.session.add(new_ad)
        await self.session.commit()