import logging
from datetime import datetime

from fastapi import APIRouter, HTTPException
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.stock.schemas import Stock as StockSchema
from src.apps.stock.schemas import StockUpdate
from src.database import Stock, fetch_one
from src.providers.market_watch import scrape_marketwatch
from src.providers.polygon import fetch_polygon_data

stock_router = APIRouter()
logger = logging.getLogger(__name__)


async def get_or_update(stock_symbol: str, date: str, session: AsyncSession) -> dict:
    polygon_data = await fetch_polygon_data(stock_symbol, date)
    marketwatch_data = await scrape_marketwatch(stock_symbol)

    stock_values = {
        "open": polygon_data["open"],
        "high": polygon_data["high"],
        "low": polygon_data["low"],
        "close": polygon_data["close"],
    }

    stock = {
        "status": "active",
        "purchased_amount": 0,
        "purchased_status": "not purchased",
        "request_date": datetime.strptime(date, "%Y-%m-%d"),
        "company_code": stock_symbol.upper(),
        "company_name": marketwatch_data["company_name"],
        "stock_values": stock_values,
        "performance_data": marketwatch_data["performance_data"],
        "competitors": marketwatch_data["competitors"],
    }

    query = select(Stock).where(Stock.company_code == stock_symbol.upper())
    result = await fetch_one(query, session)

    if result is None:
        query = insert(Stock).values(**stock).returning(Stock)
        result = await fetch_one(query, session, commit_after=True)

        if result is None:
            raise HTTPException(status_code=404, detail="Failed to insert stock data")

        return StockSchema.model_validate(result["Stock"])

    query = update(Stock).where(Stock.company_code == stock_symbol.upper()).values(**stock).returning(Stock)
    result = await fetch_one(query, session, commit_after=True)

    if result is None:
        raise HTTPException(status_code=404, detail="Failed to update stock data")

    return StockSchema.model_validate(result["Stock"])


async def update_stock(stock_symbol: str, stock_update: StockUpdate, session: AsyncSession):
    query = select(Stock).where(Stock.company_code == stock_symbol.upper())
    stock = await fetch_one(query, session)

    if stock is None:
        raise HTTPException(status_code=404, detail="Stock not found")

    updated_amount = stock_update.purchased_amount
    query = (
        update(Stock)
        .where(Stock.company_code == stock_symbol.upper())
        .values(purchased_amount=updated_amount)
        .returning(Stock)
    )
    updated_stock = await fetch_one(query, session, commit_after=True)
    return StockSchema.model_validate(updated_stock["Stock"])
