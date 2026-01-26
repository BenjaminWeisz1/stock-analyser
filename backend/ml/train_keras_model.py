import numpy as np
import pandas as pd
from pathlib import Path
from backend.ml.keras_model import train_model
from sklearn.metrics import confusion_matrix

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
model, X, y = train_model(all_returns)

# Get predicted probabilities
y_prob = model.predict(X).flatten()

# Convert probabilities to class labels
y_pred = (y_prob >= 0.5).astype(int)

# Calculate what percentage of training samples are classified correctly
accuracy = (y_pred == y).mean()
print(f"Training accuracy (manual): {accuracy:.3f}")

# Calculate what percentage of training samples would be classified correctly by only predicting the majority class
baseline_accuracy = max(
    (y == 1).mean(),
    (y == 0).mean()
)
print(f"Baseline accuracy (majority class): {baseline_accuracy:.3f}")

cm = confusion_matrix(y, y_pred)
print("Confusion matrix:")
print(cm)

print("Prediction probability stats:")
print(f"Min: {y_prob.min():.3f}")
print(f"Max: {y_prob.max():.3f}")
print(f"Mean: {y_prob.mean():.3f}")
