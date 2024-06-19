from typing import Any

from sqlalchemy import (
    JSON,
    Column,
    CursorResult,
    Date,
    Insert,
    Integer,
    MetaData,
    Select,
    String,
    Update,
)
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from src.config import settings
from src.constants import DB_NAMING_CONVENTION

DATABASE_URL = str(settings.DATABASE_ASYNC_URL)

engine = create_async_engine(DATABASE_URL)
metadata = MetaData(naming_convention=DB_NAMING_CONVENTION)
Base = declarative_base(metadata=metadata)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Stock(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String)
    purchased_amount = Column(Integer)
    purchased_status = Column(String)
    request_date = Column(Date)
    company_code = Column(String)
    company_name = Column(String)
    stock_values = Column(JSON)
    performance_data = Column(JSON)
    competitors = Column(JSON)


# Database operations
async def fetch_one(
    select_query: Select | Insert | Update,
    session: AsyncSession | None = None,
    commit_after: bool = False,
) -> dict[str, Any] | None:
    if not session:
        async with async_session() as session:
            return await _fetch_one_internal(select_query, session, commit_after)

    return await _fetch_one_internal(select_query, session, commit_after)


async def _fetch_one_internal(
    query: Select | Insert | Update,
    session: AsyncSession,
    commit_after: bool,
) -> dict[str, Any] | None:
    result = await session.execute(query)
    if commit_after:
        await session.commit()
    row = result.fetchone()
    return row._mapping if row else None


async def fetch_all(
    select_query: Select | Insert | Update,
    session: AsyncSession | None = None,
    commit_after: bool = False,
) -> list[dict[str, Any]]:
    if not session:
        async with async_session() as session:
            return await _fetch_all_internal(select_query, session, commit_after)

    return await _fetch_all_internal(select_query, session, commit_after)


async def _fetch_all_internal(
    query: Select | Insert | Update,
    session: AsyncSession,
    commit_after: bool,
) -> list[dict[str, Any]]:
    result = await session.execute(query)
    if commit_after:
        await session.commit()
    return [row._asdict() for row in result.fetchall()]


async def execute(
    query: Insert | Update,
    session: AsyncSession | None = None,
    commit_after: bool = False,
) -> None:
    if not session:
        async with async_session() as session:
            await _execute_internal(query, session, commit_after)
            return

    await _execute_internal(query, session, commit_after)


async def _execute_internal(
    query: Insert | Update,
    session: AsyncSession,
    commit_after: bool,
) -> None:
    await session.execute(query)
    if commit_after:
        await session.commit()


async def _execute_query(
    query: Select | Insert | Update,
    session: AsyncSession,
    commit_after: bool = False,
) -> CursorResult:
    result = await session.execute(query)
    if commit_after:
        await session.commit()

    return result
