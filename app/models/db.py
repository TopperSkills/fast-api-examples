from sqlalchemy.ext.asyncio import (AsyncSession,async_sessionmaker,create_async_engine)

from sqlalchemy.orm import DeclarativeBase


DB_URL="postgresql+psycopg://vedu@localhost:5432/mydb"


# database engine 
engine = create_async_engine(DB_URL,echo=True,pool_pre_ping=True)


# session factory 
AsyncSessionLocal = async_sessionmaker(bind=engine,class_=AsyncSession,expire_on_commit=False)

# Base class for all ORM models 
class Base(DeclarativeBase):
    pass

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


# to create the tables for all the database models which uses 'Base'
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)



