from datetime import date
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

import src.apps.stock.schemas as schemas
from src.apps.stock.router import stock_router


@pytest.fixture
def expected_result():
    expected_result = {
        "status": "active",
        "request_date": "2024-06-17",
        "company_code": "AAPL",
        "company_name": "Example Company",
        "stock_values": {
            "open": 213.37,
            "high": 218.95,
            "low": 212.72,
            "close": 216.67,
        },
        "performance_data": {
            "five_days": 3.45,
            "one_month": 11.41,
            "three_months": 21.7,
            "year_to_date": 11.3,
            "one_year": 15.83,
        },
        "competitors": [
            {"name": "Microsoft Corp.", "market_cap": {"value": 3.33, "currency": "$"}},
            {
                "name": "Alphabet Inc. Cl C",
                "market_cap": {"value": 2.2, "currency": "$"},
            },
            {
                "name": "Alphabet Inc. Cl A",
                "market_cap": {"value": 2.2, "currency": "$"},
            },
            {"name": "Amazon.com Inc.", "market_cap": {"value": 1.92, "currency": "$"}},
            {
                "name": "Meta Platforms Inc.",
                "market_cap": {"value": 1.29, "currency": "$"},
            },
            {
                "name": "Samsung Electronics Co. Ltd.",
                "market_cap": {"value": 528.15, "currency": "₩"},
            },
            {
                "name": "Samsung Electronics Co. Ltd. Pfd. Series 1",
                "market_cap": {"value": 528.15, "currency": "₩"},
            },
            {
                "name": "Sony Group Corp.",
                "market_cap": {"value": 15.53, "currency": "¥"},
            },
            {
                "name": "Dell Technologies Inc. Cl C",
                "market_cap": {"value": 100.73, "currency": "$"},
            },
            {"name": "HP Inc.", "market_cap": {"value": 35.16, "currency": "$"}},
        ],
        "purchased_amount": 10,
        "id": 21,
    }
    return expected_result


def test_get_stock(expected_result):
    stock_symbol = "AAPL"
    default_date = date(2022, 1, 1)

    mock_cache = MagicMock()
    mock_cache.get.return_value = expected_result

    mock_session = MagicMock(spec=AsyncSession)
    mock_session.execute.return_value.scalar.return_value = schemas.Stock(**expected_result)

    with patch(
        "src.apps.stock.router.get_or_update",
        return_value=schemas.Stock(**expected_result),
    ):
        with patch(
            "src.apps.stock.router.Config",
            return_value=MagicMock(STOCK_CACHE_EXPIRATION=60),
        ):
            with patch("src.apps.stock.router.get_default_date", return_value=default_date):
                with patch("src.apps.stock.router.get_db_session", return_value=mock_session):
                    with patch("src.apps.stock.router.get_cache", return_value=mock_cache):
                        client = TestClient(stock_router)
                        response = client.get(f"/{stock_symbol}")

    assert response.status_code == 200
    assert response.json() == expected_result


def test_update_stock(expected_result):
    stock_symbol = "AAPL"
    stock_update = schemas.StockUpdate(purchased_amount=160.0)

    mock_session = MagicMock(spec=AsyncSession)
    mock_session.execute.return_value.scalar.return_value = schemas.Stock(**expected_result)

    mock_cache = MagicMock()

    with patch(
        "src.apps.stock.router.update_stock",
        return_value=schemas.Stock(**expected_result),
    ):
        with patch("src.apps.stock.router.get_db_session", return_value=mock_session):
            with patch("src.apps.stock.router.get_cache", return_value=mock_cache):
                client = TestClient(stock_router)
                response = client.post(f"/{stock_symbol}", json=stock_update.dict())

    assert response.status_code == 200
    assert response.json() == expected_result
