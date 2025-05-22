
from sqlalchemy.future import select
from .base import session
from .models import Pin
from datetime import datetime
import Database.base_def as base_def


async def add_pin(user_id, message_id, channel_id, guild_id, add_time=None, exist=True):
    pin = Pin(user_id=user_id, message_id=message_id, channel_id=channel_id,
              guild_id=guild_id, add_time=add_time or datetime.now(), exist=exist)
    await base_def.db_add(pin)

async def check_user_id(user_id):
    async with session()as db_session, db_session.begin():
        user= await db_session.execute(select(Pin).filter(Pin.user_id==user_id))
        user = await base_def.get_all(user)
        return bool(user)

async def fetch_pin(user_id, guild_id):
    async with session()as db_session, db_session.begin():
        pin = await db_session.execute(select(Pin).filter(Pin.user_id==user_id, Pin.guild_id == guild_id).order_by(Pin.id.desc()))
        pin = await base_def.get_all(pin)
        return pin
    
async def exist_pin(user_id, message_id, channel_id, guild_id):
    async with session()as db_session, db_session.begin():
        pin = await db_session.execute(select(Pin).filter(Pin.user_id==user_id, Pin.message_id == message_id,\
                                                            Pin.channel_id==channel_id, Pin.guild_id == guild_id, Pin.exist == True))
        pin = await base_def.get_first(pin)
        return bool(pin)