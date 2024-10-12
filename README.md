# Stock Analysis Indicators

This project is a Python script that pulls stock data using the yfinance API and calculates key technical indicators used in swing trading. The results are formatted with conditional styling and saved to an HTML file, which automatically opens in the browser.

## Features
The script calculates the following technical indicators:
- **Price Rate of Change (ROC)**: Measures the percentage change in price over a 20-day period.
- **Volume Weighted Average Price (VWAP)**: Tracks the average price a stock has traded at throughout the day based on both volume and price over 10 days.
- **Weighted Moving Average (WMA)**: A moving average where more weight is placed on recent data points.
- **Hull Moving Average (HMA)**: A fast-acting moving average that reduces lag and improves smoothing.
- **Simple Moving Average (SMA)**: The average stock price over 50 days.
- **Relative Strength Index (RSI)**: A momentum oscillator that measures the speed and change of price movements (14-day window).
- **Commodity Channel Index (CCI)**: Identifies cyclical trends in stock prices (20-day window).
- **Bollinger Bands**: Measures volatility and provides upper and lower price limits (20-day window).
- **Aroon Indicator**: Measures the strength of trends and identifies potential reversals (25-day window).
- **Money Flow Index (MFI)**: A volume-weighted version of the RSI that shows buying and selling pressure (14-day window).
- **Stochastic Oscillator**: Tracks the current price in relation to its range over 14 days.

The results are saved into an HTML file with the following features:
- **Conditional Formatting**: Highlights indicator values based on predefined healthy ranges for swing trading.
    - Green: Healthy range.
    - Yellow: Average range.
    - Red: Poor range.

## How to Run the Script

### Prerequisites
- **Python 3.x**
- Required Python libraries:
    - `yfinance`
    - `pandas`
    - `matplotlib`
    - `ta-lib`
    - `seaborn`

You can install the required libraries using pip:
```bash
pip install yfinance pandas matplotlib ta seaborn




Steps to Run
Clone the repository:

git clone https://github.com/Sirpak/stock-analysis-indicators.git
cd stock-analysis-indicators

python stock_basic_technicals.py

Enter a stock ticker (e.g., AAPL, PG), and the program will download stock data and calculate the technical indicators for the past 10 rows. The formatted results will be saved in an HTML file and opened in your browser.




Output
The script generates a table of the last 10 days of technical indicators. Here's what you'll see:

OHLC data: Open, High, Low, Close, and Adjusted Close prices (rounded to 2 decimal points).
Technical indicators: Calculated indicators are highlighted based on the health of their values.
The results are saved as styled_technical_indicators.html and automatically opened in your browser.




Structure
├── stock_basic_technicals.py   # Main Python script to run the analysis
├── styled_technical_indicators.html  # Generated HTML report (auto-opened)
└── README.md                   # Project documentation




