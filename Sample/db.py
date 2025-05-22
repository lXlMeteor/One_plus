from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, DateTime, Boolean, BigInteger
from sqlalchemy.future import select
import asyncio
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os

load_dotenv()

DB_USERNAME = os.getenv("SQL_USERNAME")
DB_PASSWORD = os.getenv("SQL_PASSWORD")

DATABASE = f"postgresql+psycopg://{DB_USERNAME}:{DB_PASSWORD}@127.0.0.1:5432/test.db"
engine = create_async_engine(DATABASE, echo=True)
session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

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


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
asyncio.run(init_db())


async def db_add(data):
    async with session()as db_session, db_session.begin():
        db_session.add(data)
        await db_session.commit()

async def get_all(data):
    return data.scalars().all()

async def get_first(data):
    return data.scalars().first()


#ピン留め
async def add_Pin(user_id, message_id, channel_id, guild_id, add_time, exist):
    pin = Pin(user_id = user_id, message_id = message_id, channel_id = channel_id, guild_id = guild_id,\
                 add_time = add_time, exist = exist)
    await db_add(pin)

async def check_user_id(user_id):
    async with session()as db_session, db_session.begin():
        user= await db_session.execute(select(Pin).filter(Pin.user_id==user_id))
        user = await get_all(user)
        return bool(user)
            
async def fetch_pin(user_id, guild_id):
    async with session()as db_session, db_session.begin():
        pin = await db_session.execute(select(Pin).filter(Pin.user_id==user_id, Pin.guild_id == guild_id).order_by(Pin.id.desc()))
        pin = await get_all(pin)
        return pin

async def exist_pin(user_id, message_id, channel_id, guild_id):
    async with session()as db_session, db_session.begin():
        pin = await db_session.execute(select(Pin).filter(Pin.user_id==user_id, Pin.message_id == message_id,\
                                                            Pin.channel_id==channel_id, Pin.guild_id == guild_id, Pin.exist == True))
        pin = await get_first(pin)
        return bool(pin)


#ブラックジャック
async def coin_add(user_id, guild_id, coin):
    async with session()as db_session, db_session.begin():
        user= await db_session.execute(select(Casino_User).filter(Casino_User.user_id==user_id, Casino_User.guild_id==guild_id))
        user = await get_first(user)
        user.credit += coin
        db_session.commit()
        user= await db_session.execute(select(Casino_User).filter(Casino_User.user_id==user_id, Casino_User.guild_id==guild_id))
        user = await get_first(user)
        return user.credit
    
async def check_coin(user_id, guild_id):
    async with session()as db_session, db_session.begin():
        user= await db_session.execute(select(Casino_User).filter(Casino_User.user_id==user_id, Casino_User.guild_id==guild_id))
        user = await get_first(user)
        if user:
            return user.credit
        else:
            casino_user = Casino_User(user_id = user_id, guild_id = guild_id, add_time = datetime.now())
            await db_add(casino_user)
            return 100
            #ユーザーのデータがないので作成して、creditの値を戻す


#下書
async def draft_text_add(user_id, guild_id, text):
    async with session()as db_session, db_session.begin():
        if len(text) > 2000:
            return "文字数が2000文字を超えているため、保存できません"
        draft = await db_session.execute(select(Draft).filter(Draft.user_id == user_id, Draft.guild_id == guild_id,\
                                                               Draft.exist == True))
        draft = await get_all(draft)
        if draft and len(draft) >= 3:
            text = "下書の保存量を超えたため、保存できません"
            return text
        else:
            draft_data = Draft(user_id = user_id, guild_id = guild_id, text = text, add_time = datetime.now(), exist = True)
            await db_add(draft_data)
            return "下書の保存が完了しました"

async def draft_text_check(user_id, guild_id):
    async with session()as db_session, db_session.begin():
        draft = await db_session.execute(select(Draft).filter(Draft.user_id == user_id, Draft.guild_id == guild_id,\
                                                               Draft.exist == True))
        draft = await get_all(draft)

        text = ""
        for i, d in enumerate(draft):
            text += f"{i+1}.\n"
            if len(d.text) >= 300:
                draft_text = f"{d.text[0:300]}..."
            else:
                draft_text = d.text
            text += f"{draft_text}\n\n"

        text += "\n\n下書の全文を確認するためには、コマンド'/draft 下書番号'を実行してください"
        
        return text

async def draft_text_selected(user_id, guild_id,number):
    async with session()as db_session, db_session.begin():
        draft = await db_session.execute(select(Draft).filter(Draft.user_id == user_id, Draft.guild_id == guild_id,\
                                                               Draft.exist == True))
        draft = await get_all(draft)

        text = ""

        text += f"{draft[number-1].text}"

        return text

async def draft_text_delete(user_id, guild_id,number):
    try:
        async with session()as db_session, db_session.begin():
            draft = await db_session.execute(select(Draft).filter(Draft.user_id == user_id, Draft.guild_id == guild_id,\
                                                                Draft.exist == True))
            draft = await get_all(draft)

            draft[number-1].exist = False
            await db_session.commit()

            text = "選択した下書を削除しました"

            return text
    except AttributeError as e:
        print(e)
        return "選択した下書の削除に失敗しました"

