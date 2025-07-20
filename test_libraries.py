import yfinance as yf
from datetime import datetime, timedelta

# Test yfinance for stock data
try:
    vymi = yf.Ticker("VYMI")
    hist = vymi.history(period="5y")
    print("Successfully fetched stock data for VYMI:")
    print(hist.head())
except Exception as e:
    print(f"Failed to fetch stock data: {e}")

# Test yfinance for currency rates
try:
    eurusd = yf.Ticker("EURUSD=X")
    eurusd_hist = eurusd.history(period="5y")
    print("\nSuccessfully fetched currency rates for EUR/USD:")
    print(eurusd_hist.head())
except Exception as e:
    print(f"Failed to fetch currency rates: {e}")
