# stock-analyser
Project for a full-stack web application that allows users to analyse stocks using historical market data

## Running the app
- To run the backend, run the following command in the terminal: uvicorn backend.main:app --reload
- To run the frontend, open frontend/index.html with live server in VS Code

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
- If a request has been processed before, cached results are returned to avoid redundant API calls