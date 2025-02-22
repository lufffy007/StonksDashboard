from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from app.database.database import Base

class Stock(Base):
    __tablename__ = "stocks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    symbol: Mapped[str] = mapped_column(String, index=True)
    quantity: Mapped[float] = mapped_column(Float)
    buy_price: Mapped[float] = mapped_column(Float)
    current_price: Mapped[float] = mapped_column(Float, nullable=True)  # This might be null initially
    pnl: Mapped[float] = mapped_column(Float, nullable=True)
