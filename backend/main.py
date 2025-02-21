from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from typing import List

app = FastAPI()

# Allow CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

stocks = [
    {"symbol": "AAPL", "quantity": 10, "buyPrice": 150, "currentPrice": 175},
    {"symbol": "GOOG", "quantity": 5, "buyPrice": 2800, "currentPrice": 2950},
    {"symbol": "AMZN", "quantity": 2, "buyPrice": 3500, "currentPrice": 3400},
]

@app.get("/api/stocks", response_model=List[dict])
def get_stocks():
    return stocks

@app.get("/")
def read_root():
    return {"message": "Stock Dashboard Backend"} 