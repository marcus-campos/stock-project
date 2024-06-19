import logging

import httpx

from src.config import Config

config = Config()
logger = logging.getLogger(__name__)


async def fetch_polygon_data(stock_symbol: str, date: str):
    url = f"https://api.polygon.io/v1/open-close/{stock_symbol.upper()}/{date}"
    params = {"apiKey": config.POLYGON_API_KEY}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)

        if response.status_code == 401:
            logger.error("Unauthorized access. Check if additional headers or cookies are needed.")
            return
        elif response.status_code == 403:
            logger.error("Forbidden access. Check if the API key is valid.")
            return
        elif response.status_code != 200:
            logger.error(f"Failed to fetch data from Polygon API: {response.text}")
            return

        return response.json()
