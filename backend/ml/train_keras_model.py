import numpy as np
import pandas as pd
from pathlib import Path
from backend.ml.keras_model import train_model

# Get the path to the saved csv files used for training the model
DATA_DIR = Path(__file__).resolve().parent / "data"

all_returns = []

# For each stock in the training data, get the returns on each day
for csv_file in DATA_DIR.glob("*.csv"):
    df = pd.read_csv(csv_file)
    closes = df["close"].astype(float).values
    returns = (closes[1:] - closes[:-1]) / closes[:-1]
    all_returns.extend(returns)

all_returns = np.array(returns)

# Train the model on combined returns for each stock in the training data
model = train_model(all_returns)