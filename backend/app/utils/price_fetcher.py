from alpha_vantage.timeseries import TimeSeries
import requests
import time 
import random   


price_cache = {}
cache_expiry= {}
CACHE_DURATION =300

def get_live_price(symbol:str, exchange: str, max_retries:int =3 ) -> float:
    current_time = time.time()  
    cache_key = f"{symbol}_{exchange}"

    if cache_key in price_cache and cache_expiry.get(cache_key,0)>current_time:
        print(f"Using cached Price for {symbol}")
        return price_cache [cache_key]


    ts = TimeSeries(key='3YYDEUEBAN89V548',output_format='json')    

    for attempt in range(max_retries):
        try:
            if exchange=="NSE": 
                symbol_av=f"{symbol}.NSE"
            else:
                symbol_av= symbol
            
            data, _ = ts.get_quote_endpoint(symbol=symbol_av)

            # Check for API errors
            if 'Error Message' in data:
                raise ValueError(data['Error Message'])

            # Extract the price
            price = float(data['05. price'])

            # Store in cache
            price_cache[cache_key] = price
            cache_expiry[cache_key] = current_time + CACHE_DURATION
            print(f"Fetched live price for {symbol}: {price}")
            return price

        except Exception as e:
            print(f"Attempt {attempt + 1}/{max_retries} - Error for {symbol}: {e}")
            # Handle rate limits with exponential backoff
            if "rate limit" in str(e).lower() or "too many requests" in str(e).lower():
                if attempt < max_retries - 1:
                    wait_time = (2 ** attempt) + random.uniform(0, 1)
                    print(f"Rate limited, waiting {wait_time:.2f} seconds")
                    time.sleep(wait_time)
                else:
                    print("Max retries reached: Rate limit exceeded")
            else:
                print(f"Failed to fetch price for {symbol}: {e}")

            # Fallback to cached price if available
            if cache_key in price_cache:
                print(f"Using expired cache for {symbol}")
                return price_cache[cache_key]
            # Return None if no price is available
            return None

# Test the function
if __name__ == "__main__":
    price = get_live_price("AAPL", "NASDAQ")
    if price is not None:
        print(f"AAPL price: {price} USD")
    else:
        print("Failed to fetch AAPL price")


    