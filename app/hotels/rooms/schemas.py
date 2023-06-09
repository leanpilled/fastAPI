from pydantic import BaseModel
from sqlalchemy import JSON


class SRoom(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: str
    price: int
    services: JSON
    quantity: int
    image_id: int
    
    class Config:
        orm_mode = True