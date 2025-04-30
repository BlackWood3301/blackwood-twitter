from fastapi import APIRouter,HTTPException, Depends
from app.user.schemas import SUSser, LoginUser
from app.user.dao import UserDao
from app.user.auth import get_password_hash,verify_password,create_access_token, get_current_user

app = APIRouter(prefix="/user",tags=["Регистрация и авторизация"])

@app.post("/register")
async def register_user(user:SUSser):

    user_ = await UserDao.find_one_or_none(email = user.email)
    if user_:
        raise HTTPException(status_code=403,detail="User already registered")
    
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

@app.post("/login")
async def login(user: LoginUser):
    user_ = await UserDao.find_one_or_none(email=user.email)
    if not user_:
        raise HTTPException(status_code=401, detail="Неверный email или пароль")
    
    # Проверяем пароль
    if not verify_password(user.password, user_.password):
        raise HTTPException(status_code=401, detail="Неверный email или пароль")
    
    # Создаем токен
    token = create_access_token({"sub": str(user_.id)})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/me")
async def get_current_user_info(current_user = Depends(get_current_user)):
    return current_user