from datetime import date
from fastapi import APIRouter
from app.hotels.rooms.dao import RoomsDAO

router = APIRouter(
    prefix="",
    tags=["Rooms"]
)

@router.get("/hotels/{hotel_id}/rooms")
async def get_rooms(hotel_id:int, date_from: date, date_to: date):
    return await RoomsDAO.get_rooms(hotel_id, date_from, date_to)