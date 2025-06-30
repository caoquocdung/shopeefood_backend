from pydantic import BaseModel
from typing import Optional

class CategoryCreate(BaseModel):
    name: str
    description: Optional[str] = None
    image_url: Optional[str] = None

class CategoryUpdate(BaseModel):
    category_id: int
    name: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None

class CategoryResponse(BaseModel):
    category_id: int
    name: str
    description: Optional[str]
    image_url: Optional[str]

    class Config:
        from_attributes = True