from dotenv import load_dotenv
import os
import requests

# Load environment variables
load_dotenv()

# Load the API key
ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')

if not ALPHA_VANTAGE_API_KEY:
    raise RuntimeError("ALPHA_VANTAGE_API_KEY not found in environment")

# Fetch all the historical data for a given stock from the API
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