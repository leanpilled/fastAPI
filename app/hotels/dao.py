from datetime import date
from app.bookings.models import Bookings

from app.dao.base import BaseDAO
from sqlalchemy import select, and_, or_, func
from app.hotels.rooms.models import Rooms
from app.db import async_session_maker
from app.hotels.models import Hotels

class HotelsDAO(BaseDAO):
    model = Hotels
    
    @classmethod
    async def get_all_hotels(cls, location: str, date_from: date, date_to: date):
        async with async_session_maker() as session:
            """with booked_rooms as (
                select * from bookings
                where 
                (date_from >= '2023-05-13' and date_from <= '2023-07-20') or
                (date_from <= '2023-05-13' and date_to > '2023-05-13')
                ),

                booked as
                (select hotel_id, count(rooms.id) as booked from booked_rooms
                left join rooms on booked_rooms.room_id=rooms.id
                group by rooms.id)
                                    
                select id, name, location, services, rooms_quantity, image_id, rooms_quantity-COALESCE(booked, 0 ) as rooms_left from hotels
                left join booked on hotels.id = booked.hotel_id
                WHERE location LIKE '%Коми%'"""
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
            
            booked_per_hotel = select(
                func.count(booked_rooms.c.id).label("booked"),
                Rooms.hotel_id,
            ).select_from(
                booked_rooms
            ).join(
                Rooms, Rooms.id == booked_rooms.c.room_id, isouter=True
            ).group_by(
                Rooms.id
            ).subquery()
            
            query = select(
                Hotels.id, 
                Hotels.name, 
                Hotels.location, 
                Hotels.services, 
                Hotels.rooms_quantity, 
                Hotels.image_id, 
                (Hotels.rooms_quantity - func.COALESCE(booked_per_hotel.c.booked, 0 )).label("rooms_left")
            ).select_from(Hotels).join(
                booked_per_hotel, Hotels.id == booked_per_hotel.c.hotel_id, isouter=True
            ).filter(Hotels.location.like(f'%{location}%')).distinct(Hotels.id)
            
            hotels = await session.execute(query)
            return hotels.mappings().all()