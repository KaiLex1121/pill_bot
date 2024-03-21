from app.dao.base import BaseDAO
from sqlalchemy.ext.asyncio import AsyncSession
from models.database.advertisement import Advertisment


class UserDAO(BaseDAO[Advertisment]):
    def __init__(self, session: AsyncSession):
        super().__init__(Advertisment, session)
