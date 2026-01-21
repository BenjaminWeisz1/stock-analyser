from fastapi.middleware.cors import CORSMiddleware
from backend.auth.routes import router as auth_router
from backend.auth.security import require_auth
from backend.db.database import init_db
from fastapi import FastAPI, Depends
from dotenv import load_dotenv
import os
import requests

# Load environment variables
load_dotenv()

# Load the API key
ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')

if not ALPHA_VANTAGE_API_KEY:
    raise RuntimeError("ALPHA_VANTAGE_API_KEY not found in environment")

def fetch_daily_stock_data(symbol: str):
    url = "https://www.alphavantage.co/query"

    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "apikey": ALPHA_VANTAGE_API_KEY
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()

    if "Time Series (Daily)" not in data:
        raise ValueError(f"Invalid response from Alpha Vantage: {data}")

    return data["Time Series (Daily)"]

init_db()

app = FastAPI()

app.include_router(auth_router)

# Indicate the port used in development
# Update in Phase 5
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Root endpoint
@app.get("/")
def root():
    return {"status": "Stock Analyser API running"}


# List all the stocks
# Update in phase 5
@app.get("/stocks/list")
def get_list():
    return ["AAPL", "GOOG", "IBM", "MSFT", "NPXI", "PANW", "PYPL", "TSLA"]

# Show the financial information associated with a stock
@app.post("/stocks/analyze")
def analyze_stock(stock: str, date: str | None = None, user_email: str = Depends(require_auth)):
    series = fetch_daily_stock_data(stock)

    # Sort dates (newest first)
    dates = sorted(series.keys(), reverse=True)

    if date is None:
        date = dates[0]

    if date not in series:
        raise ValueError(f"No data available for {date}")

    idx = dates.index(date)

    if idx + 1 >= len(dates):
        raise ValueError("Cannot compute returns for earliest available date")

    today = series[date]
    prev_day = series[dates[idx + 1]]

    close_today = float(today["4. close"])
    close_prev = float(prev_day["4. close"])

    returns = (close_today - close_prev) / close_prev

    volume = int(today["5. volume"])

    return {
        "name": stock,
        "date": date,
        "price": close_today,
        "returns": returns,
        "volume": volume,
        "trend": "Green"  # still dummy
    }
