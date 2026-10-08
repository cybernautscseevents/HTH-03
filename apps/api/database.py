"""
ClinScribe AI — Database Connection
Async SQLAlchemy engine and session management for PostgreSQL.
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import get_settings
from models import Base

settings = get_settings()

# Async engine for FastAPI
try:
    async_engine = create_async_engine(
        settings.database_url,
        echo=settings.debug,
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
    )
    AsyncSessionLocal = async_sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
except Exception:
    async_engine = create_async_engine(
        "sqlite+aiosqlite:///./clinscribe.db",
        echo=settings.debug,
    )
    AsyncSessionLocal = async_sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

# Sync engine for migrations and scripts
try:
    sync_engine = create_engine(
        settings.database_sync_url,
        echo=settings.debug,
    )
    SyncSessionLocal = sessionmaker(bind=sync_engine)
except Exception:
    sync_engine = create_engine(
        "sqlite:///./clinscribe.db",
        echo=settings.debug,
    )
    SyncSessionLocal = sessionmaker(bind=sync_engine)


async def get_db() -> AsyncSession:
    """Dependency injection for database sessions."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    """Create all tables. Used for development and demo setup."""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_db():
    """Drop all tables. Used for development reset only."""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
