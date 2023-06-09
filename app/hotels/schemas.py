from pydantic import BaseModel
from sqlalchemy import JSON


class SHotel(BaseModel):
    id: int
    name: str
    location: str
    services: JSON
    rooms_quantity: int
    image_id: int
    
    class Config:
        orm_mode = True