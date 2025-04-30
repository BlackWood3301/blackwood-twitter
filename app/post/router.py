from fastapi import APIRouter, Depends, HTTPException
from app.post.dao import PostDao
from app.post.schemas import SPost
from app.user.auth import get_current_user
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = APIRouter(prefix="/post", tags=["Посты"])

@app.get("/")
async def get_all_post():
    try:
        logger.info("Запрос на получение всех постов")
        posts = await PostDao.find_all()
        logger.info(f"Получено {len(posts)} постов")
        
        # Отладим структуру данных
        if posts and len(posts) > 0:
            first_post = posts[0]
            logger.info(f"Структура первого поста: {first_post}")
            logger.info(f"Ключи первого поста: {first_post.keys() if hasattr(first_post, 'keys') else 'нет метода keys'}")
        
        # Преобразуем посты в список словарей для лучшей сериализации
        formatted_posts = []
        for post_dict in posts:
            try:
                # Извлекаем объект Post из словаря {'Post': <Post object>}
                post = post_dict['Post'] if 'Post' in post_dict else post_dict
                
                # Теперь работаем с объектом модели post
                formatted_post = {
                    "id": post.id if hasattr(post, 'id') else None,
                    "description": post.description if hasattr(post, 'description') else "",
                    "like": post.like if hasattr(post, 'like') else 0,
                    "user_id": post.user_id if hasattr(post, 'user_id') else None,
                    "created_at": post.created_at.isoformat() if hasattr(post, 'created_at') and post.created_at else None
                }
                
                formatted_posts.append(formatted_post)
            except Exception as post_error:
                logger.error(f"Ошибка при обработке поста: {str(post_error)}")
                # Пропускаем проблемный пост и продолжаем обработку остальных
                continue
                
        return formatted_posts
    except Exception as e:
        logger.error(f"Ошибка при получении постов: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка сервера: {str(e)}")

@app.post("/add")
async def add_post(post: SPost, user=Depends(get_current_user)):
    try:
        logger.info(f"Запрос на создание поста: {post.description[:50]}...")
        result = await PostDao.add_date(
            description=post.description,
            like=post.like,
            user_id=user.id
        )
        logger.info(f"Пост успешно создан с ID: {result.id}")
        return result
    except Exception as e:
        logger.error(f"Ошибка при создании поста: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Не удалось создать пост: {str(e)}")
    
@app.post("/like/{post_id}")
async def add_like(post_id: int):
    try:
        logger.info(f"Запрос на увеличение лайка для поста ID:{post_id}")
        
        # Вызываем метод DAO для увеличения количества лайков
        updated_post = await PostDao.like_for_post(post_id)
        
        if not updated_post:
            raise HTTPException(status_code=404, detail="Пост не найден")
        
        # Возвращаем обновленные данные поста
        return {
            "id": updated_post.id,
            "description": updated_post.description,
            "like": updated_post.like,
            "user_id": updated_post.user_id,
            "created_at": updated_post.created_at.isoformat() if hasattr(updated_post, 'created_at') and updated_post.created_at else None
        }
    except Exception as e:
        logger.error(f"Ошибка при добавлении лайка: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Не удалось добавить лайк: {str(e)}")

@app.post("/dislike/{post_id}")
async def remove_like(post_id: int):
    try:
        logger.info(f"Запрос на удаление лайка для поста ID:{post_id}")
        
        # Вызываем метод DAO для уменьшения количества лайков
        updated_post = await PostDao.dislike_for_post(post_id)
        
        if not updated_post:
            raise HTTPException(status_code=404, detail="Пост не найден")
        
        # Возвращаем обновленные данные поста
        return {
            "id": updated_post.id,
            "description": updated_post.description,
            "like": updated_post.like,
            "user_id": updated_post.user_id,
            "created_at": updated_post.created_at.isoformat() if hasattr(updated_post, 'created_at') and updated_post.created_at else None
        }
    except Exception as e:
        logger.error(f"Ошибка при удалении лайка: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Не удалось удалить лайк: {str(e)}")