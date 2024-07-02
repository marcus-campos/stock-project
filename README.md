## Stock Project Documentation

### Overview
This project is built using [FastAPI](https://fastapi.tiangolo.com/) and follows the best practices outlined in [FastAPI Best Practices](https://github.com/zhanymkanov/fastapi-best-practices). The structure is organized in bundles to maintain a modular and scalable codebase.

### Project Structure
```
stock-project
├── alembic/
├── infra/
├── src
│   ├── apps
│   │   ├── stock
│   │   │   ├── constants.py
│   │   │   ├── dependencies.py
│   │   │   ├── exceptions.py
│   │   │   ├── router.py
│   │   │   ├── schemas.py
│   │   │   └── service.py
│   ├── providers
│   │   ├── market_watch.py
│   │   └── polygon.py
│   ├── tests
│   │   └── test_stock.py
│   ├── cache.py 
│   ├── config.py
│   ├── constants.py
│   ├── database.py
│   ├── dependencies.py
│   ├── exceptions.py
│   ├── main.py
│   └── utils.py
├── .env
├── .env.example
├── .gitignore
├── alembic.ini
├── docker-compose.prod.yml
├── docker-compose.yml
├── justfile
├── LICENSE
├── logging_production.ini
├── logging.ini
├── poetry.lock
├── pyproject.toml
├── README.md
└── ruff.toml
```

### Challenge Summary

#### Goal
The assignment is to implement a Stocks REST API using Python and a popular web framework of your choice (e.g., FastAPI, Flask, Django). The API will retrieve stock data from an external financial API and perform minor data scraping from the Marketwatch financial website.

#### Requirements
- **Language:** Python (3.10 or above)
- **API:** REST API returning JSON responses
- **Project Structure:** Follow best practices
- **Repository:** Commit all code into a GitHub repository with a README.md containing instructions and a technical overview
- **Model:** Implement a Stock model with the following attributes:
  - Status (String)
  - purchased_amount (Integer)
  - purchased_status (String)
  - request_data (Date in YYYY-MM-DD format)
  - company_code (String)
  - company_name (String)
  - Stock_values (Object)
    - open (Float)
    - high (Float)
    - low (Float)
    - close (Float)
  - performance_data (Object)
    - five_days (Float)
    - one_month (Float)
    - three_months (Float)
    - year_to_date (Float)
    - one_year (Float)
  - Competitors (Array[Object])
    - name (String)
    - market_cap (Object)
      - Currency (String)
      - Value (Float)

- **Endpoints:**
  - **[GET] /stock/{stock_symbol}:** Returns the stock data for the given symbol
  - **[POST] /stock/{stock_symbol}:** Updates the stock entity with the purchased amount

- **Caching:** Implement caching per stock mechanism on the GET route
- **Database:** Implement data persistence into a PostgresDB for stocks and their purchased amounts
- **Docker:** Create a Dockerfile for the API application
- **Logging:** Implement logs for the application
- **Unit Tests:** Write unit tests to ensure correctness

#### Sources
- **Polygon.io:** Retrieve daily stock data
  - Endpoint: `/v1/open-close/{stocksTicker}/{date}`
  - API Key: `<your_api_key>`
  - Documentation: [Polygon.io Docs](https://polygon.io/docs/stocks/get_v1_open-close__stocksticker___date)
- **MarketWatch:** Scrape performance and competitors data from the stock page
  - Example URL: `https://www.marketwatch.com/investing/stock/aapl`

### Setup Instructions

#### Installing Just
- **MacOS:**
  ```shell
  brew install just
  ```

- **Debian/Ubuntu:**
  ```shell
  apt install just
  ```

- **Others:** [Just Installation Packages](https://github.com/casey/just?tab=readme-ov-file#packages)

#### Installing Poetry
```shell
pip install poetry
```

- **Other Methods:** [Poetry Installation](https://python-poetry.org/docs/#installation)

#### Environment Setup and Dependency Installation
1. Copy the example environment file:
   ```shell
   cp .env.example .env
   ```
2. Edit the `.env` file and add your configuration settings, such as keys from Polygon.
3. Install the dependencies:
   ```shell
   poetry install
   ```

### Running the Application

#### Using Just
```shell
just up
```

#### Running Uvicorn Server Directly
- With default settings:
  ```shell
  just run
  ```

- With additional configurations (e.g., logging file):
  ```shell
  just run --log-config logging.ini
  ```

### Linters
To format the code:
```shell
just lint
```

### Database Migrations
- **Create a migration:**
  ```shell
  just mm *migration_name*
  ```

- **Run migrations:**
  ```shell
  just migrate
  ```

- **Downgrade migrations:**
  ```shell
  just downgrade downgrade -1  # or -2, base, or migration hash
  ```

### Deployment
Deployment is handled using Docker and Gunicorn. The Dockerfile is optimized for a small image size and fast builds, using a non-root user. Gunicorn is configured to use the number of workers based on the available CPU cores.

**Example: Running the app with Docker Compose**
```shell
cp .env.example .env
```
Edit the `.env` file and add your configuration settings, such as keys from Polygon.

Ensure that Docker is installed and running on your machine. Then, run the following command:
```shell
docker compose -f docker-compose.prod.yml up -d --build
```