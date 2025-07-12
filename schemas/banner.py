from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

from models import BannerStatus


class BannerCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: BannerStatus = BannerStatus.active
    image_url: str

class BannerUpdate(BaseModel):
    banner_id: int
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[BannerStatus] = None
    image_url: Optional[str] = None

class BannerResponse(BaseModel):
    banner_id: int
    title: str
    description: Optional[str]
    status: BannerStatus
    image_url: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
