from fastapi import FastAPI

app = FastAPI()

'''
# POST request to register
@app.post("/auth/register")
def register():

# POST request to login
@app.post("/auth/login")
def login():
'''

# Root endpoint
@app.get("/")
def root():
    return {"status": "Stock Analyser API running"}


# List all the stocks
@app.get("/stocks/list")
def get_list():
    return ["BHG", "GLN", "AGL", "NPN"]

# Show the financial information associated with a stock
@app.post("/stocks/analyze")
def analyze_stock(stock: str):
    return {
        "name": "BTI",
        "date": "2026-01-19T18:27:00.000Z",
        "price": 200,
        "returns": 250,
        "volume": 1,
        "trend": "Green"
    }
