from fastapi import FastAPI
from app.user.router import app as user_router

app = FastAPI()
app.include_router(user_router)

