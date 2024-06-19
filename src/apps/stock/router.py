import json
import logging
from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import src.apps.stock.schemas as schemas
from src.apps.stock.dependencies import get_default_date
from src.apps.stock.service import get_or_update, update_stock
from src.config import Config
from src.dependencies import get_cache, get_db_session

stock_router = APIRouter()
logger = logging.getLogger(__name__)


@stock_router.get("/{stock_symbol}", response_model=schemas.Stock)
async def get_stock(
    stock_symbol: str,
    date: date = Depends(get_default_date),
    session: AsyncSession = Depends(get_db_session),
    cache=Depends(get_cache),
):
    if result := await cache.get(stock_symbol):
        return json.loads(result)

    result = await get_or_update(stock_symbol, date, session)
    await cache.set(stock_symbol, result.json(), ex=Config().STOCK_CACHE_EXPIRATION)

    return result


@stock_router.post("/{stock_symbol}", response_model=schemas.Stock)
async def update(
    stock_symbol: str,
    stock_update: schemas.StockUpdate,
    session: AsyncSession = Depends(get_db_session),
    cache=Depends(get_cache),
):
    updated_stock = await update_stock(stock_symbol, stock_update, session)
    await cache.set(stock_symbol, updated_stock.json(), ex=Config().STOCK_CACHE_EXPIRATION)
    return updated_stock
