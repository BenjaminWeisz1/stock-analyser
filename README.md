# Stock Analyser
This project is a full-stack stock analysis web application built to demonstrate end-to-end system design, combining
- backend APIs
- authentication
- external data integration
- machine learning
- database caching
- frontend UI
- production deployment

This app allows users to register, login, select a stock and date, and receive:
- historical price data
- daily returns
- volume
- a machine-learning-based trend prediction (green=increasing, red=decreasing)

## High-level architecture
**Frontend (HTML/CSS/JavaScript)**
↓
**FastAPI Backend (Python)**
↓
**SQLite Cache+ML Model**
↓
**Alpha Vantage Market Data API**

The frontend and backend are hosted together and communicate via HTTP requests.

## Authentication
- Users must login or register to have access to stock data
- Each password is salted and hashed using SHA-256 before storage in SQLite
- Authentication is required to access stock analysis endpoints

## Data source
- Alpha Vantage is used as a source for historical stock market data
- Alpha Vantage API key is stored in a .env file in the backend

## Stock Data Pipeline
1. The user selects a stock symbol and a date
2. The backend checks a local SQLite cache.
   If not cached, it fetches historical data from Alpha Vantage
3. The backend computes closing price, daily returns and volume
4. Results are cached to reduce API usage

This design avoids unnecessary API calls and improves performance.

## Machine Learning for Trend Prediction
A simple feed-forward neural network is used to predict whether a stock is likely to be increasing (green) or decreasing (red)

### Model overview
- Implemented using Keras
- Input: last 30 daily returns for a stock
- Output: binary classification as to whether the returns the next day were positive (increasing) or negative (decreasing)
- Architecture uses dense layers with ReLU activation and sigmoid output for probability estimation

### Training process
- The model is trained offline using historical stock data
- The model is trained on many stocks to improve generalisation
- Run backend/ml/download_stock_data.py to download daily price data from Alpha Vantage and store locally as CSV files
- Run backend/ml/train_keras_model.py to train the model on this data and save the results to backend/ml/keras_model.h5
- Training includes basic evaluation metrics such as accuracy, confusion matrix and baseline comparison

## Caching
- Stock analysis results are cached in a SQLite database to reduce API usage
- Trend predictions are not cached
- Instead, each analysis computes the trend using the currently loaded model to avoid stale predictions

## Frontend UI
The frontend is a single-page interface that:
- handles authentication
- allows stock/date selection
- displays results in a clear, readable format
- highlights trend predictions visually (green/red)
- shows meaningful error messages when data is unavailable

## Deployment
The application is deployed using Render and runs continuously:
- Backend: FastAPI
- Frontend: served as static files by FastAPI
- Environment variables used for API keys

**Live URL**:
https://stock-analyser-y343.onrender.com/static/index.html


