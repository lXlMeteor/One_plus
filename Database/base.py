
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import asyncio, os, sys

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

load_dotenv()

DB_USERNAME = os.getenv("SQL_USERNAME")
DB_PASSWORD = os.getenv("SQL_PASSWORD")

DATABASE = f"postgresql+psycopg://{DB_USERNAME}:{DB_PASSWORD}@localhost:5432/test.db"
engine = create_async_engine(DATABASE, echo=True)
session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(init_db())
