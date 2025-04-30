from pydantic import BaseModel,EmailStr
from typing import Annotated

class SUSser(BaseModel):

    image: Annotated[str, (0, 255)]
    nick_name: str
    name: str
    email:EmailStr
    password: str

class LoginUser(BaseModel):
    email: EmailStr
    password: str