"""Initialize database tables."""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.ext.asyncio import create_async_engine
from db.database import DATABASE_URL
from db.models import Base, User, Interview, Article

async def init_database():
    """Create all database tables."""
    # Create engine
    engine = create_async_engine(DATABASE_URL, echo=True)
    
    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    print("✅ Database tables created successfully!")
    
    # Close engine
    await engine.dispose()

async def drop_all_tables():
    """Drop all database tables (use with caution!)."""
    engine = create_async_engine(DATABASE_URL, echo=True)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    print("⚠️  All database tables dropped!")
    await engine.dispose()

if __name__ == "__main__":
    # Run initialization
    asyncio.run(init_database()) 