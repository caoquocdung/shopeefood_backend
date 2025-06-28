from pydantic import BaseModel
from typing import Optional

class AddressCreate(BaseModel):
    uid: str
    receiver: str
    phone: str
    address: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    is_default: Optional[bool] = False

class AddressUpdate(BaseModel):
    address_id: int
    receiver: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    is_default: Optional[bool] = None

class AddressResponse(BaseModel):
    address_id: int
    uid: str
    receiver: str
    phone: str
    address: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    is_default: bool

    class Config:
        from_attributes = True