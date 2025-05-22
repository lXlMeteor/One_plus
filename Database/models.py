
from sqlalchemy import Column, Integer, String, DateTime, Boolean, BigInteger

from .base import Base

class Pin(Base):
    __tablename__ = "pin"
    id = Column(Integer, primary_key=True, index = True)
    user_id = Column(BigInteger, nullable=False)
    message_id = Column(BigInteger, nullable=False)
    channel_id = Column(BigInteger, nullable=False)
    guild_id = Column(BigInteger, nullable=False)
    add_time = Column(DateTime, nullable=False)
    exist = Column(Boolean, nullable=False)

class Casino_User(Base):
    __tablename__ = "casino_user"
    id = Column(Integer, primary_key=True, index = True)
    user_id = Column(BigInteger, nullable=False)
    guild_id = Column(BigInteger, nullable=False)
    credit = Column(BigInteger, nullable=False,default=100)
    add_time = Column(DateTime, nullable=False)

class Draft(Base):
    __tablename__ = "draft"
    id = Column(Integer, primary_key=True, index = True)
    user_id = Column(BigInteger, nullable=False)
    guild_id = Column(BigInteger, nullable=False)
    text = Column(String(2000),nullable=False)
    add_time = Column(DateTime, nullable=False)
    exist = Column(Boolean, nullable=False)