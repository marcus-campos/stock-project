# Create your dependencies here

from datetime import date, datetime, timedelta


async def get_default_date(date: str = None) -> date:
    if not date:
        return (datetime.now() - timedelta(days=1)).date().isoformat()

    return datetime.strptime(date, "%Y-%m-%d").date().isoformat()
