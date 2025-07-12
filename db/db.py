from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession
from config import Config
from sqlmodel import create_engine, SQLModel

engine: AsyncEngine = AsyncEngine(create_engine(
    Config.DATABASE_URL,
    echo=True,
    future=True
))

async def get_session() :
    async with AsyncSession(engine) as session:
        yield session
async def init_db():
    """Import database."""
    try:
        print("Starting database initialization...")
        async with engine.begin() as conn:
            from schemas import USER
            from schemas.blog import BlogPost, Image
            await conn.run_sync(SQLModel.metadata.create_all)
        print("Database initialization completed successfully")
    except Exception as e:
        print(f"Error initializing database: {str(e)}")
        raise