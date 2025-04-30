from fastapi import APIRouter, HTTPException, Depends, Response
from app.user.schemas import SUSser, LoginUser
from app.user.dao import UserDao
from app.user.auth import get_password_hash, verify_password, create_access_token, get_current_user
import logging
import traceback

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = APIRouter(prefix="/user", tags=["Регистрация и авторизация"])

@app.post("/register")
async def register_user(user:SUSser):
    try:
        user_ = await UserDao.find_one_or_none(email = user.email)
        if user_:
            raise HTTPException(status_code=403, detail="User already registered")
        
        password_hash = get_password_hash(user.password)
        await UserDao.add_date(
            image=user.image,
            nike_name=user.nick_name,
            name=user.name,
            email=user.email,
            password=password_hash
        )
        user_ = await UserDao.find_one_or_none(email = user.email)
        token = create_access_token({"sub": str(user_.id)})
        return {"message": "User registered successfully", "access_token": token, "token_type": "bearer"}
    except Exception as e:
        logger.error(f"Ошибка при регистрации: {str(e)}")
        logger.error(traceback.format_exc())
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Ошибка при регистрации: {str(e)}")

@app.post("/login")
async def login(user: LoginUser, response: Response):
    try:
        user_ = await UserDao.find_one_or_none(email=user.email)
        if not user_:
            raise HTTPException(status_code=401, detail="Неверный email")
        
        # Проверяем пароль
        if not verify_password(user.password, user_.password):
            raise HTTPException(status_code=401, detail="Неверный пароль")
        
        # Создаем токен
        token = create_access_token({"sub": str(user_.id)})
        
        response.set_cookie(
            key="user_id", 
            value=token,
            httponly=True,
            secure=False,  # Для локальной разработки без HTTPS
            samesite="lax",
            max_age=1800  # 30 минут в секундах
        )
        return {"access_token": token, "token_type": "bearer"}
    except Exception as e:
        logger.error(f"Ошибка при входе: {str(e)}")
        logger.error(traceback.format_exc())
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Ошибка при входе: {str(e)}")

@app.get("/me")
async def get_current_user_info(current_user = Depends(get_current_user)):
    try:
        logger.info(f"Запрос информации о пользователе ID:{getattr(current_user, 'id', 'N/A')}")
        
        # Преобразуем пользователя в словарь для безопасной сериализации
        user_dict = {
            "id": getattr(current_user, 'id', None),
            "name": getattr(current_user, 'name', ""),
            "nick_name": getattr(current_user, 'nike_name', ""),
            "email": getattr(current_user, 'email', ""),
            "image": getattr(current_user, 'image', "")
        }
        
        logger.info(f"Возвращаем данные пользователя: {user_dict}")
        return user_dict
    except Exception as e:
        logger.error(f"Ошибка при получении данных пользователя: {str(e)}")
        logger.error(traceback.format_exc())
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Ошибка при получении данных пользователя: {str(e)}")

@app.post("/logout")
async def logout(response: Response):
    try:
        # Удаляем куки, устанавливая пустое значение и время жизни 0
        response.delete_cookie(
            key="user_id",
            httponly=True,
            secure=False,  # Для локальной разработки без HTTPS
            samesite="lax"
        )
        return {"message": "Вы успешно вышли из системы"}
    except Exception as e:
        logger.error(f"Ошибка при выходе: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Ошибка при выходе: {str(e)}")

@app.get("/{user_id}")
async def get_user_by_id(user_id: int, current_user = Depends(get_current_user)):
    try:
        logger.info(f"Запрос информации о пользователе ID:{user_id}")
        
        # Получаем пользователя из базы данных по ID
        user = await UserDao.find_one_or_none(id=user_id)
        
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        
        # Преобразуем пользователя в словарь для безопасной сериализации
        user_dict = {
            "id": getattr(user, 'id', None),
            "name": getattr(user, 'name', ""),
            "nick_name": getattr(user, 'nike_name', ""),
            "email": getattr(user, 'email', ""),
            "image": getattr(user, 'image', "")
        }
        
        logger.info(f"Возвращаем данные пользователя: {user_dict}")
        return user_dict
    except Exception as e:
        logger.error(f"Ошибка при получении данных пользователя: {str(e)}")
        logger.error(traceback.format_exc())
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Ошибка при получении данных пользователя: {str(e)}")

