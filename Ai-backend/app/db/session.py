from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import get_settings

settings = get_settings()

# Fallback to sqlite if no DB URL is adequately configured, or use the provided one.
# For now we use the one from settings.
# Note: For SQLite use "sqlite+aiosqlite:///./test.db"
DATABASE_URL = settings.DATABASE_URL or "sqlite+aiosqlite:///./sql_app.db"

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
