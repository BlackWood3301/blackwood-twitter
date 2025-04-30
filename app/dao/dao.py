from sqlalchemy import select,delete,insert,update
from app.database import session

class BaseDao:
    model = None

    @classmethod
    async def add_date(cls,**value):
        async with session.begin() as sess:
            query = insert(cls.model).values(**value).returning(cls.model)
            result = await sess.execute(query)
            return result.scalar_one()
    
    @classmethod
    async def find_one_or_none(cls,**find):
        async with session.begin() as sess:
            query = select(cls.model).filter_by(**find)
            result = await sess.execute(query)
            return result.scalar_one_or_none()
        
    @classmethod
    async def find_all(cls,**filter):
        async with session.begin() as sess:
            query = select(cls.model).filter_by(**filter)
            result = await sess.execute(query)
            return result.mappings().all()