from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

# Explicitly load environment variables
load_dotenv()

# Use a simple relative path for SQLite database
DATABASE_URL = "sqlite+aiosqlite:///./interviewer.db"

print(f"Using DATABASE_URL: {DATABASE_URL}")

# Create Base for declarative models
Base = declarative_base()

# Create engine with SQLite-compatible configuration
engine = create_async_engine(
    DATABASE_URL, 
    echo=True, 
    future=True,
    # SQLite specific configuration
    connect_args={
        "check_same_thread": False,
        "timeout": 30,
    }
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Add this function for async table creation
async def create_all_tables():
    from db.models import Base
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
