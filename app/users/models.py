from sqlalchemy import Column, Integer, String
from app.db import Base


class Users(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)