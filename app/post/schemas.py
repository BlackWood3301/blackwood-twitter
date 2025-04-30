from pydantic import BaseModel
from typing import Optional

class SPost(BaseModel):
    
    description: str
    like: int
    user_id: Optional[int] = None