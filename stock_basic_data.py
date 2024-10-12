# -*- coding: utf-8 -*-
"""
A python script that pulls stock data including Adjusted Close, OHLC, Volume, Dividends, and Financials.

@author: David Czerepak
"""

import datetime as dt
import yfinance as yf
import pandas as pd
from datetime import datetime

# Get the stock ticker from user input
ticker = input("Enter the ticker of the stock: ")
print(f"The stock you chose is: {ticker}")

# Define the start and end dates (past 10 years)
start = datetime.today() - dt.timedelta(days=3650)  # 10 years
end = datetime.today()

# Download Adjusted Close prices
print("Downloading Adjusted Close prices...")
adj_close_data = pd.DataFrame()
adj_close_data[ticker] = yf.download(ticker, start=start, end=end)["Adj Close"]
print("Adjusted Close prices downloaded.\n")

# Download OHLC and Volume data
print("Downloading OHLC and Volume data...")
ohlc_volume_data = yf.download(ticker, start=start, end=end)[["Open", "High", "Low", "Close", "Volume"]]
print("OHLC and Volume data downloaded.\n")

# Download Dividends data
print("Downloading Dividends data...")
dividends_data = yf.Ticker(ticker).dividends
print("Dividends data downloaded.\n")

# Download Financials (Optional: Uncomment if you want to include this)
print("Downloading Financials data...")
stock = yf.Ticker(ticker)
financials_data = stock.financials
print("Financials data downloaded.\n")

# Show the first few rows of each dataset
print("First 5 rows of Adjusted Close prices:")
print(adj_close_data.head())

print("\nFirst 5 rows of OHLC and Volume data:")
print(ohlc_volume_data.head())

print("\nDividends data (if any):")
print(dividends_data.head())

print("\nFinancials data (Optional, showing a sample of financial statements):")
print(financials_data.head())
