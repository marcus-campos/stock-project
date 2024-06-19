import logging
import re

import httpx
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


async def scrape_marketwatch(stock_symbol: str):
    url = f"https://www.marketwatch.com/investing/stock/{stock_symbol.lower()}?mod=search_symbol"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Accept-Language": "pt-BR,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": "max-age=0",
    }

    async with httpx.AsyncClient(headers=headers) as client:
        response = await client.get(url)
        if response.status_code == 401:
            logger.error("Unauthorized access. Check if additional headers or cookies are needed.")
            return

        soup = BeautifulSoup(response.content, "html.parser")

        performance_data = {
            "five_days": 0.0,
            "one_month": 0.0,
            "three_months": 0.0,
            "year_to_date": 0.0,
            "one_year": 0.0,
        }
        
        try:
            company_name = soup.find("h1", class_="company__name").text.strip()
        except Exception as e:
            logger.error(f"Error parsing name: {e}")
        
        try:
            performance_section = soup.find("div", class_="element element--table performance")
            if performance_section:
                rows = performance_section.find_all("tr", class_="table__row")
                period_mapping = {
                    "5 Day": "five_days",
                    "1 Month": "one_month",
                    "3 Month": "three_months",
                    "YTD": "year_to_date",
                    "1 Year": "one_year",
                }
                for row in rows:
                    cells = row.find_all("td", class_="table__cell")
                    if cells and len(cells) == 2:
                        period = cells[0].text.strip()
                        value = cells[1].find("li", class_="content__item value ignore-color").text.strip("%")
                        if period in period_mapping:
                            performance_data[period_mapping[period]] = float(value)
        except Exception as e:
            logger.error(f"Error parsing performance data: {e}")

        competitors = []
        try:
            competitors_section = soup.find("table", {"aria-label": "Competitors data table"})
            if competitors_section:
                rows = competitors_section.find("tbody").find_all("tr", class_="table__row")
                for row in rows:
                    cells = row.find_all("td")
                    if cells and len(cells) == 3:
                        name = cells[0].text.strip()
                        market_cap = cells[2].text.strip()

                        market_cap_match = re.match(r"([^\d]+)?([\d.,]+)([^\d]+)?", market_cap)
                        if market_cap_match:
                            currency = market_cap_match.group(1) or market_cap_match.group(3) or ""
                            numeric_value = market_cap_match.group(2).replace(",", "")
                            market_cap_numeric = float(numeric_value)

                            competitor = {
                                "name": name,
                                "market_cap": {
                                    "value": market_cap_numeric,
                                    "currency": currency,
                                },
                            }
                            competitors.append(competitor)
        except Exception as e:
            logger.error(f"Error parsing competitors data: {e}")

        return {"performance_data": performance_data, "competitors": competitors, "company_name": company_name}
