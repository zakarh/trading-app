# data_fetcher.py
import pandas as pd
import datetime
import pandas_datareader.data as web
import yfinance as yf
from config import ALPACA_API_KEY, ALPACA_API_SECRET, ALPACA_BASE_URL
import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import TimeFrame 

def fetch_historical_data(symbol, start_date, end_date):
    """
    Fetch historical data for a given symbol using Yahoo Finance.
    """
    try:
        df = yf.download(symbol, start=start_date, end=end_date)
        return df
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None

def initialize_alpaca_api():
    """
    Initialize and return an Alpaca API connection.
    """
    try:
        api = tradeapi.REST(ALPACA_API_KEY, ALPACA_API_SECRET, ALPACA_BASE_URL, api_version='v2')
        return api
    except Exception as e:
        print(f"Error initializing Alpaca API: {e}")
        return None

def fetch_live_data(api, symbol):
    """
    Fetch the latest live bar data for a given symbol using Alpaca.
    """
    try:
        barset = api.get_bars(symbol, TimeFrame.Minute, limit=1)
        data = barset[0]
        live_data = {
            'time': data.t,
            'open': data.o,
            'high': data.h,
            'low': data.l,
            'close': data.c,
            'volume': data.v
        }
        return live_data
    except Exception as e:
        print(f"Error fetching live data for {symbol}: {e}")
        return None

if __name__ == '__main__':
    # Example usage
    start = datetime.datetime(2020, 1, 1)
    end = datetime.datetime(2021, 1, 1)
    symbol = 'AAPL'
    df = fetch_historical_data(symbol, start, end)
    if df is not None:
        print(df.head())
