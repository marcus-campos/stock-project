from datetime import date
from typing import List

from pydantic import BaseModel


class StockValues(BaseModel):
    open: float
    high: float
    low: float
    close: float


class PerformanceData(BaseModel):
    five_days: float
    one_month: float
    three_months: float
    year_to_date: float
    one_year: float


class MarketCap(BaseModel):
    value: float
    currency: str


class Competitor(BaseModel):
    name: str
    market_cap: MarketCap


class StockBase(BaseModel):
    status: str
    request_date: date
    company_code: str
    company_name: str
    stock_values: StockValues
    performance_data: PerformanceData
    competitors: List[Competitor]
    purchased_amount: int


class StockCreate(StockBase):
    purchased_amount: int
    purchased_status: str


class StockUpdate(BaseModel):
    purchased_amount: int


class Stock(StockBase):
    id: int

    class Config:
        from_attributes = True
