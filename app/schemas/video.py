from pydantic import BaseModel
from typing import Optional


class VideoCreate(BaseModel):
    title: str
    description: Optional[str] = None
    is_paid: bool = False
    price: Optional[float] = None


class VideoResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    is_paid: bool
    price: Optional[float]
    status: str

class VideoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_paid: Optional[bool] = None
    price: Optional[float] = None


class VideoStatusUpdate(BaseModel):
    status: str  # UPLOADED, PROCESSING, READY