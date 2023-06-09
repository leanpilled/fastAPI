from datetime import date
from app.bookings.models import Bookings

from app.dao.base import BaseDAO
from sqlalchemy import select, and_, or_, func
from app.hotels.rooms.models import Rooms
from app.db import async_session_maker
from app.hotels.models import Hotels

class RoomsDAO(BaseDAO):
    model = Hotels
    
    @classmethod
    async def get_rooms(cls, hotel_id:int, date_from: date, date_to: date):
        async with async_session_maker() as session:
            
            booked_rooms = select(Bookings).where(
                    or_(
                        and_(
                            Bookings.date_from >= date_from,
                            Bookings.date_from <= date_to
                        ),
                        and_(
                            Bookings.date_from <= date_from,
                            Bookings.date_to > date_from
                        )
                    )
                ).subquery()
            
            """with booked_rooms as (
            select room_id from bookings
            where 
            (date_from >= '2023-05-13' and date_from <= '2023-07-20') or
            (date_from <= '2023-05-13' and date_to > '2023-05-13')
            ),

            booked as
            (select rooms.id, count(rooms.id) as booked from booked_rooms
            left join rooms on booked_rooms.room_id=rooms.id
            group by rooms.id)
                                
            select rooms.id, rooms.hotel_id, quantity, quantity-COALESCE(booked, 0 ) as rooms_left from rooms
            left join booked on rooms.id = booked.id
            where hotel_id=1"""
            
            booked = select(
                func.count(booked_rooms.c.id).label("rooms_left"),
                Rooms.id,
            ).select_from(
                booked_rooms
            ).join(
                Rooms, Rooms.id == booked_rooms.c.room_id, isouter=True
            ).group_by(
                Rooms.id
            ).subquery()
            
            query = select(
                Rooms.id,
                Rooms.hotel_id,
                Rooms.name,
                Rooms.description,
                Rooms.services,
                Rooms.price,
                Rooms.quantity,
                Rooms.image_id,
                (Rooms.quantity - func.COALESCE(booked.c.rooms_left, 0 )).label("rooms_left")
            ).select_from(Rooms).join(
                booked, Rooms.id == booked.c.id, isouter=True
            ).where(Rooms.hotel_id == hotel_id)
            
            rooms = await session.execute(query)
            return rooms.mappings().all()