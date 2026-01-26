# stock-analyser
Project for a full-stack web application that allows users to analyse stocks using historical market data

## Running the app
- Run the following command in the terminal: uvicorn backend.main:app --reload
- Then to see the frontend, open http://127.0.0.1:8000/static/index.html in the browser

## Features
- User registration and login with salted SHA-256 password hashing
- Real-time stock data retrieval via Alpha Vantage
- SQLite caching to reduce API calls
- Authenticated access to stock analysis endpoints
- Simple HTML/JavaScript frontend

## Data source
- Alpha Vantage is used as a source for historical stock market data
- Alpha Vantage API key is stored in a .env file in the backend

## Authentication
- Users must login or register to have access to stock data
- Each password is salted and hashed using SHA-256 before storage in SQLite

## Caching
- Stock analysis results are cached in a SQLite database
- Trend predictions are not cached
- Each analysis computes the trend using the currently loaded model to avoid stale predictions

## Neural network
Use a simple feed-forward neural network for predicting short-term stock trends

### Model overview
- Implemented using Keras
- Input: last 30 daily returns for a stock
- Output: binary classification as to whether the returns the next day were positive (increasing) or negative (decreasing)

### Training process
- The model is trained offline using historical market data
- Run backend/ml/download_stock_data.py to download daily price data from Alpha Vantage and store locally as CSV files
- Run backend/ml/train_keras_model.py to train the model on this data and save the results to backend/ml/keras_model.h5
- Training includes basic evaluation metrics such as accuracy, confusion matrix and baseline comparison