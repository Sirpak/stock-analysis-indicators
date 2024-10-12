import datetime as dt
import yfinance as yf
import pandas as pd
import ta
from datetime import datetime
import matplotlib.pyplot as plt
import webbrowser

# Hull Moving Average (HMA) Calculation
def HMA(data, period=20):
    half_length = int(period / 2)
    sqrt_length = int(period ** 0.5)

    # Weighted Moving Average (WMA) calculations for half and full periods
    wma_half = ta.trend.WMAIndicator(data['Close'], window=half_length).wma()
    wma_full = ta.trend.WMAIndicator(data['Close'], window=period).wma()

    # Hull Moving Average calculation
    diff = 2 * wma_half - wma_full
    hma = ta.trend.WMAIndicator(pd.Series(diff), window=sqrt_length).wma()
    
    return hma

# Helper function to color based on health
def highlight_cells(val, col_name):
    # Define healthy ranges based on swing trading strategy
    healthy_ranges = {
        'ROC': (-5, 5),   # A small range is considered healthy
        'RSI': (30, 70),  # RSI between 30-70 is generally considered healthy
        'CCI': (-100, 100), # Healthy CCI ranges
        'MFI': (20, 80),  # MFI healthy range between 20 and 80
        'Stoch_K': (20, 80), # Stochastic Oscillator healthy range
        'VWAP': (None, None), # VWAP does not have a strict healthy range
        'WMA': (None, None), # WMA value is used for trend analysis
        'HMA': (None, None),
        'SMA': (None, None),
        'Aroon_Up': (70, 100),  # Aroon Up healthy if > 70
        'Aroon_Down': (0, 30)   # Aroon Down healthy if < 30
    }

    # Get healthy range
    low, high = healthy_ranges.get(col_name, (None, None))

    try:
        if low is not None and high is not None:
            if low <= float(val.strip('%$')) <= high:
                return 'background-color: green'  # Healthy
            elif float(val.strip('%$')) < low or float(val.strip('%$')) > high:
                return 'background-color: red'  # Poor
            else:
                return 'background-color: yellow'  # Average
        else:
            return ''  # No color for undefined healthy range
    except:
        return ''  # Handle cases where value cannot be converted to float

# Get the stock ticker from user input
ticker = input("Enter the ticker of the stock: ")
print(f"The stock you chose is: {ticker}")

# Download the stock data
end_date = datetime.today().strftime('%Y-%m-%d')
data = yf.download(ticker, start="2023-01-01", end=end_date)

# Round OHLC and Adj Close columns to 2 decimal places
data[['Open', 'High', 'Low', 'Close', 'Adj Close']] = data[['Open', 'High', 'Low', 'Close', 'Adj Close']].round(2)

# Calculate indicators for swing trading

# Rate of change for past 20 days (more appropriate for swing trading)
data['ROC'] = data['Close'].pct_change(periods=20) * 100

# VWAP over 10 trading days (swing trading)
window_size = 10
data['VWAP'] = (data['Volume'] * (data['High'] + data['Low'] + data['Close']) / 3).rolling(window=window_size).sum() / data['Volume'].rolling(window=window_size).sum()

# Moving averages
data['WMA'] = ta.trend.WMAIndicator(close=data['Close'], window=20).wma()
data['HMA'] = HMA(data, period=20)
data['SMA'] = data['Close'].rolling(window=50).mean()

# RSI with 14 days
data['RSI'] = ta.momentum.RSIIndicator(close=data['Close'], window=14).rsi()

# CCI with 20 days
data['CCI'] = ta.trend.CCIIndicator(high=data['High'], low=data['Low'], close=data['Close'], window=20).cci()

# Bollinger Bands
bb = ta.volatility.BollingerBands(close=data['Close'], window=20, window_dev=2)
data['BB_High'] = bb.bollinger_hband()
data['BB_Low'] = bb.bollinger_lband()

# Aroon Indicator
aroon = ta.trend.AroonIndicator(high=data['High'], low=data['Low'], window=25)
data['Aroon_Up'] = aroon.aroon_up()
data['Aroon_Down'] = aroon.aroon_down()

# Money Flow Index (MFI)
data['MFI'] = ta.volume.MFIIndicator(high=data['High'], low=data['Low'], close=data['Close'], volume=data['Volume'], window=14).money_flow_index()

# Stochastic Oscillator
stoch = ta.momentum.StochasticOscillator(high=data['High'], low=data['Low'], close=data['Close'], window=14)
data['Stoch_K'] = stoch.stoch()
data['Stoch_D'] = stoch.stoch_signal()

# Select the last few rows to show as a table
subset = data.tail(10)

# Format the table with appropriate number formats
tech_indicators = subset[['ROC', 'VWAP', 'WMA', 'HMA', 'SMA', 'RSI', 'CCI', 'BB_High', 'BB_Low', 'Aroon_Up', 'Aroon_Down', 'MFI', 'Stoch_K', 'Stoch_D']].copy()

tech_indicators['ROC'] = tech_indicators['ROC'].apply(lambda x: "{:.2f}%".format(x))
tech_indicators['VWAP'] = tech_indicators['VWAP'].apply(lambda x: "${:,.2f}".format(x))
tech_indicators['WMA'] = tech_indicators['WMA'].apply(lambda x: "${:,.2f}".format(x))
tech_indicators['HMA'] = tech_indicators['HMA'].apply(lambda x: "${:,.2f}".format(x))
tech_indicators['SMA'] = tech_indicators['SMA'].apply(lambda x: "${:,.2f}".format(x))
tech_indicators['RSI'] = tech_indicators['RSI'].apply(lambda x: "{:.2f}".format(x))
tech_indicators['CCI'] = tech_indicators['CCI'].apply(lambda x: "{:.2f}".format(x))
tech_indicators['BB_High'] = tech_indicators['BB_High'].apply(lambda x: "${:,.2f}".format(x))
tech_indicators['BB_Low'] = tech_indicators['BB_Low'].apply(lambda x: "${:,.2f}".format(x))
tech_indicators['Aroon_Up'] = tech_indicators['Aroon_Up'].apply(lambda x: "{:.0f}".format(x))
tech_indicators['Aroon_Down'] = tech_indicators['Aroon_Down'].apply(lambda x: "{:.0f}".format(x))
tech_indicators['MFI'] = tech_indicators['MFI'].apply(lambda x: "{:.2f}".format(x))
tech_indicators['Stoch_K'] = tech_indicators['Stoch_K'].apply(lambda x: "{:.2f}".format(x))
tech_indicators['Stoch_D'] = tech_indicators['Stoch_D'].apply(lambda x: "{:.2f}".format(x))

# Apply conditional formatting using Styler.apply (column-based logic)
def style_func(row):
    return [highlight_cells(row[col], col) for col in row.index]

styled_tech_indicators = tech_indicators.style.apply(style_func, axis=1)

# Save the styled DataFrame as an HTML file
html_file = 'styled_technical_indicators.html'
styled_tech_indicators.to_html(html_file)

# Open the file in the default browser
webbrowser.open_new_tab(html_file)

print(f"Styled table has been saved and opened in your browser: {html_file}")


