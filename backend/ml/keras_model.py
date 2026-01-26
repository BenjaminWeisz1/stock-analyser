import pandas as pd
import numpy as np
from keras.models import Sequential, load_model
from keras.layers import Dense
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Convert an array of daily returns into a dataset
def create_dataset(returns, window=30):
    X = []
    y = []

    for i in range(window, len(returns)):
        # Input: returns of the 30 days before day i
        X.append(returns[i-window:i])

        # Label: direction of the return on day i
        y.append(1 if returns[i] > 0 else 0)
    
    return np.array(X), np.array(y)


# Build a feed-forward neural network
def build_model(input_size = 30):
    '''
    Input layer: 30 daily returns
    Hidden layer 1: 32 neurons with ReLU activation
    Hidden layer 2: 16 neurons with ReLU activation
    Output layer: 1 neuron with sigmoid activation to squeeze the probability between 0 and 1
    '''
    model = Sequential([
        Dense(32, activation="relu", input_shape=(input_size,)),
        Dense(16, activation="relu"),
        Dense(1, activation="sigmoid")
    ])

    # Update the weights and biases to minimize error according to a cross-entropy loss function
    model.compile(
        optimizer="adam",
        loss="binary_crossentropy",
        metrics=["accuracy"]
    )

    return model

# Train the neural network on historical return data
# Sample = 30 consecutive daily returns
# batch_size = how many samples are processed together before the model updates its weights
# epoch = one complete pass through the entire training set
# The model will see every sample 20 times, but each time with slightly updated weights
def train_model(returns, epochs = 20, batch_size = 32):
    X, y = create_dataset(returns)

    model = build_model(input_size=X.shape[1])

    model.fit(
        X,
        y,
        epochs=epochs,
        batch_size=batch_size,
        validation_split=0.2, # 80% training data, 20% testing data
        verbose=1
    )

    model.save("backend/ml/keras_model.h5")
    return model, X, y

def load_trained_model():
    return load_model("backend/ml/keras_model.h5")

# Use the trained model to predict the trend for the next day
def predict_trend(model, last_30_returns):
    last_30_returns = last_30_returns.reshape(1, -1)
    probability = model.predict(last_30_returns)[0][0]
    return 1 if probability >= 0.5 else 0