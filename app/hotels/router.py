from datetime import date
from fastapi import APIRouter
from app.hotels.dao import HotelsDAO
from fastapi_cache.decorator import cache

router = APIRouter(
    prefix="/hotels",
    tags=["Hotels"]
)

@router.get("/{location}")
@cache(expire=60)
async def get_all_hotels(location: str, date_from: date, date_to: date):
    return await HotelsDAO.get_all_hotels(location, date_from, date_to)

@router.get("/id/{hotel_id}")
async def get_hotel(hotel_id: int):
    return await HotelsDAO.find_by_id(hotel_id)