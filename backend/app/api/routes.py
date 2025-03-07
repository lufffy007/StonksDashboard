from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.stock import Stock
from app.database.database import SessionLocal, engine
from pydantic import BaseModel, confloat
from app.utils.price_fetcher import get_live_price
from sqlalchemy.exc import SQLAlchemyError  # Make sure to import this

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic model for request validation
class StockCreate(BaseModel):
    symbol: str
    quantity: confloat(gt=0)  # type: ignore
    buy_price: confloat(gt=0) # type: ignore
    exchange: str  # Could add enum validation

class StockResponse(BaseModel):
    id: int
    symbol: str
    quantity: float
    buy_price: float
    current_price: float
    pnl: float
    exchange: str
    
    class Config:
        from_attributes = True  # For Pydantic v2
        # If you're using Pydantic v1, use orm_mode = True instead

@router.post("/stocks/", response_model=StockResponse)
def add_stock(stock: StockCreate, db: Session = Depends(get_db)):
    print(f"Recieved Stock: {stock}")
    # Rest of your function stays the same
    # Validate symbol exists and fetch live price using data from the StockCreate model
    try:
        price = get_live_price(stock.symbol, stock.exchange)
        if price <= 0:
            raise HTTPException(status_code=400, detail="Invalid symbol or exchange")
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Invalid stock data",
                 "errors": [str(e)]  # Wrap in array for consistent format
                   }
)
    
    # Create a new Stock instance with the provided data and the fetched price
    db_stock = Stock(
        symbol=stock.symbol,
        quantity=stock.quantity,
        buy_price=stock.buy_price,
        exchange=stock.exchange,
        current_price=price,  # store the fetched live price
        pnl=(price - stock.buy_price) * stock.quantity  # calculate profit/loss
    )
    db.add(db_stock)
    db.commit()
    db.refresh(db_stock)
    return db_stock

@router.get("/stocks/", response_model=list[StockResponse])
def get_stocks(db: Session = Depends(get_db)):
    try:
        stocks = db.query(Stock).all()
        for stock in stocks:
            stock.current_price = get_live_price(stock.symbol, stock.exchange)
            stock.pnl = (stock.current_price - stock.buy_price) * stock.quantity
        return stocks
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error")

@router.delete("/stocks/{stock_id}")
def delete_stock(stock_id: int, db: Session = Depends(get_db)):
    stock = db.query(Stock).filter(Stock.id == stock_id).first()
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    db.delete(stock)
    db.commit()
    return {"message": "Stock deleted"}
