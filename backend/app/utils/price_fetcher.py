import yfinance as yf
from nsepy import get_quote

def get_live_price(symbol: str, exchange: str) -> float:
    try:
        if exchange in ["NASDAQ", "TSX"]:
            ticker = yf.Ticker(symbol)
            return ticker.history(period="1d")["Close"].iloc[-1]
        elif exchange == "NSE":
            return get_quote(symbol)["lastPrice"]
        else:
            return 0.0  # Handle other exchanges later
    except Exception as e:
        print(f"Error fetching price for {symbol}: {e}")
        return 0.0