from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.stock import Stock
from app.database.database import SessionLocal, engine

from app.utils.price_fetcher import get_live_price

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/stocks/")
def add_stock(symbol: str, quantity: float, buy_price: float, exchange: str, db: Session = Depends(get_db)):
    # Validate input (example: check if symbol exists)
    db_stock = Stock(symbol=symbol, quantity=quantity, buy_price=buy_price, exchange=exchange)
    db.add(db_stock)
    db.commit()
    db.refresh(db_stock)
    return db_stock

@router.get("/stocks/")
def get_stocks(db: Session = Depends(get_db)):
    stocks = db.query(Stock).all()
    for stock in stocks:
        stock.current_price = get_live_price(stock.symbol, stock.exchange)
        stock.pnl = (stock.current_price - stock.buy_price) * stock.quantity
    return stocks

@router.delete("/stocks/{stock_id}")
def delete_stock(stock_id: int, db: Session = Depends(get_db)):
    stock = db.query(Stock).filter(Stock.id == stock_id).first()
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    db.delete(stock)
    db.commit()
    return {"message": "Stock deleted"}

