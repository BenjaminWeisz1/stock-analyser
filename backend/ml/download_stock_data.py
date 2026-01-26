import csv
import time
from pathlib import Path
from backend.data.alphavantage import fetch_daily_stock_data

# Stocks to train the neural network on
SYMBOLS = []

# Make a path for the historical data to be saved in the data folder
DATA_DIR = Path(__file__).resolve().parent / "data"
DATA_DIR.mkdir(exist_ok=True)

for i, symbol in enumerate(SYMBOLS):
    print(f"Downloading {symbol}...")

    # Get the historical data for the stock from the API
    series = fetch_daily_stock_data(symbol)

    csv_path = DATA_DIR / f"{symbol}.csv"

    # Write the historical data for each stock to its own csv file in the data folder
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "open", "high", "low", "close", "volume"])

        for date in sorted(series.keys()):
            day = series[date]
            writer.writerow([
                date,
                day["1. open"],
                day["2. high"],
                day["3. low"],
                day["4. close"],
                day["5. volume"],
            ])
    
    # Sleep in between requests so as not to exceed the API call limit
    if i < len(SYMBOLS)-1:
        time.sleep(15)

    print(f"Saved to {csv_path}")
