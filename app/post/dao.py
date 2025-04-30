from app.dao.dao import BaseDao
from app.post.model import Post
from app.database import session
from sqlalchemy import select,delete,insert,update

class PostDao(BaseDao):
    model = Post

    @classmethod
    async def like_for_post(cls, post_id: int):
        async with session.begin() as sess:
            # Сначала найдем пост по id
            query = select(cls.model).filter_by(id=post_id)
            result = await sess.execute(query)
            post = result.scalar_one_or_none()
            
            if not post:
                return None
                
            # Увеличиваем количество лайков на 1
            post.like += 1
            
            # Сохраняем изменения в базе данных
            await sess.commit()
            
            return post
        
    @classmethod
    async def dislike_for_post(cls, post_id: int):
        async with session.begin() as sess:
            # Сначала найдем пост по id
            query = select(cls.model).filter_by(id=post_id)
            result = await sess.execute(query)
            post = result.scalar_one_or_none()
            
            if not post:
                return None
                
            # Увеличиваем количество лайков на 1
            post.like -= 1
            
            # Сохраняем изменения в базе данных
            await sess.commit()
            
            return post