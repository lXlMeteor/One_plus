
from sqlalchemy.future import select
from .base import session
from .models import Casino_User
from datetime import datetime
import Database.base_def as base_def

#ブラックジャック
async def coin_add(user_id, guild_id, coin):
    async with session()as db_session, db_session.begin():

        user= await db_session.execute(select(Casino_User).filter(Casino_User.user_id==user_id, Casino_User.guild_id==guild_id))
        user = await base_def.get_first(user)

        user.credit += coin
        db_session.commit()

        user= await db_session.execute(select(Casino_User).filter(Casino_User.user_id==user_id, Casino_User.guild_id==guild_id))
        user = await base_def.get_first(user)

        return user.credit
    
async def check_coin(user_id, guild_id):
    async with session()as db_session, db_session.begin():

        user= await db_session.execute(select(Casino_User).filter(Casino_User.user_id==user_id, Casino_User.guild_id==guild_id))
        user = await base_def.get_first(user)

        if user:

            return user.credit
        
        else:

            casino_user = Casino_User(user_id = user_id, guild_id = guild_id, add_time = datetime.now())
            await base_def.db_add(casino_user)
            return 100
            #ユーザーのデータがないので作成して、creditの値を戻す