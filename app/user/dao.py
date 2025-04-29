from app.dao.dao import BaseDao
from app.user.model import User

class UserDao(BaseDao):
    model = User