from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, DateTime, func
from datetime import datetime

class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str]
    like: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), server_default=func.now())

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    
    # Добавляем отношение к пользователю
    user: Mapped["User"] = relationship("User", back_populates="posts")