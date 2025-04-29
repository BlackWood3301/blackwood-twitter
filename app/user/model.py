from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from sqlalchemy import String, DateTime
from pydantic import EmailStr



class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key = True)
    image: Mapped[str] = mapped_column(String(255))
    nike_name: Mapped[str]
    name: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]
