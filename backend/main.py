from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import numpy as np
from backend.data.alphavantage import fetch_daily_stock_data
from backend.auth.routes import router as auth_router
from backend.auth.security import require_auth
from backend.db.database import init_db, get_cached_stock, insert_cached_stock
from backend.ml.keras_model import load_trained_model, predict_trend

init_db()

app = FastAPI()

app.include_router(auth_router)

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

app.mount("/static", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")

# Load the neural network model
model = load_trained_model()

# Convert daily price series into an array of daily returns ordered from oldest to newest
def compute_returns_from_series(series):
    dates = sorted(series.keys())
    closes = [float(series[d]["4. close"]) for d in dates]

    returns = []
    for i in range(1, len(closes)):
        r = (closes[i] - closes[i - 1]) / closes[i - 1]
        returns.append(r)

    return returns, dates[1:]  # returns aligned with dates


# Root endpoint
@app.get("/")
def root():
    return {"status": "Stock Analyser API running"}


# List all the stocks
@app.get("/stocks/list")
def get_list():
    return ["AAPL", "GOOG", "IBM", "META", "MSFT", "PANW", "PYPL", "TSLA"]

# Show the financial information associated with a stock
@app.post("/stocks/analyze")
def analyze_stock(stock: str, date: str, user_email: str = Depends(require_auth)):
    # Fetch the stock from API
    series = fetch_daily_stock_data(stock)

    # Sort dates from oldest to newest
    dates = sorted(series.keys())

    if date not in series:
        raise ValueError(f"No data available for {date}")

    idx = dates.index(date)

    if idx + 1 >= len(dates):
        raise ValueError("Cannot compute returns for earliest available date")

    # Check if stock is in cache
    cached = get_cached_stock(stock, date)
    
    if cached:
        close_today = cached["price"]
        returns = cached["returns"]
        volume = cached["volume"]
    else:
        today = series[date]
        prev_day = series[dates[idx - 1]]

        close_today = float(today["4. close"])
        close_prev = float(prev_day["4. close"])

        returns = (close_today - close_prev) / close_prev
        volume = int(today["5. volume"])

        # Cache the result
        insert_cached_stock(stock, date, close_today, returns, volume)

    closes = [float(series[d]["4. close"]) for d in dates[:idx + 1]]

    if len(closes) < 31:
        raise ValueError("Not enough historical data for neural network prediction")

    daily_returns = [
        (closes[i] - closes[i - 1]) / closes[i - 1]
        for i in range(1, len(closes))
    ]

    last_30_returns = np.array(daily_returns[-30:])

    trend_label = predict_trend(model, last_30_returns)
    trend = "green" if trend_label == 1 else "red"
    
    # Predict trend using trained neural network
    trend_label = predict_trend(model, last_30_returns)
    trend = "green" if trend_label == 1 else "red"

    return {
        "name": stock,
        "date": date,
        "price": close_today,
        "returns": returns,
        "volume": volume,
        "trend": trend,
    }