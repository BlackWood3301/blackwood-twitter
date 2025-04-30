from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.user.router import app as user_router
from app.post.router import app as post_router
import os

app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://localhost:3000", "http://localhost:5000", "http://127.0.0.1:3000", "http://127.0.0.1:5000"],  # Добавлены типичные порты для фронтенда
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение API роутеров
app.include_router(user_router)
app.include_router(post_router)

# Монтирование статических файлов
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Корневой маршрут будет отдавать index.html
@app.get("/")
async def read_index():
    return FileResponse("frontend/index.html")

# Маршрут для страницы входа
@app.get("/login")
async def read_login():
    return FileResponse("frontend/login.html")

# Маршрут для страницы регистрации
@app.get("/signup")
async def read_signup():
    return FileResponse("frontend/signup.html")

# Маршрут для страницы ленты
@app.get("/feed")
async def read_feed():
    return FileResponse("frontend/feed.html")

