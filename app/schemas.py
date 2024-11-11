from pydantic import BaseModel
from typing import Optional


class PostSchema(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True
    rating: int = None