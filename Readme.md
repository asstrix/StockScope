# StockScope

StockScope is a Python application for retrieving, analyzing, and exporting stock price data using the Yahoo Finance API. 
This program enables you to fetch historical data, compute statistical indicators, and export results for further analysis. 
The application includes functions for data visualization, moving averages, and calculating key financial metrics like MACD and RSI.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Functions](#functions)

## Features

- **Fetch stock data** for specified tickers and periods using Yahoo Finance.
- **Calculate statistical indicators** such as mean, variance, and standard deviation of stock prices.
- **Add financial indicators** like Moving Average (MA), MACD, and RSI to the data.
- **Export data to CSV** for offline analysis.
- **Export data to HTML** for data visualization.
- **Threshold-based alerts** for price fluctuations.
- **Console output** with human-readable descriptions of the analysis results.

## Installation

To run StockScope, you need Python 3.x and the required packages. Clone this repository and install dependencies:

git clone https://github.com/asstrix/StockScope.git<br>
cd StockScope<br>
pip install -r requirements.txt<br>
run main.py in cmd


Usage
Initialize the Logger: Set up logging to track program actions.<br>
Specify Ticker and Period: Input the stock ticker and desired period (e.g., 'AAPL' and '1mo').<br>
Call Functions: Use functions such as fetch_stock_data, add_moving_average, or calculate_rsi to analyze the data.<br>
Export Results: Export data to a CSV file with export_to_csv.<br>

# Initialize logger
logger = logging.getLogger(__name__)<br>
logging.basicConfig(level=logging.DEBUG)

# Fetch data
data = fetch_stock_data(logger, ticker="AAPL", period="1mo")

# Add moving average
add_moving_average(logger, data, window_size=20)

# Export to CSV
export_to_csv(logger, data, ticker="AAPL", period="1mo")<br>
Configuration<br>
Adjust settings as needed:<br>

Period codes: Adjusted with period_spell function for custom periods like '1d', '1mo', or date ranges.<br>
Logger: Configure logging level and format in the main script for additional debugging.<br>
Thresholds: Define price fluctuation thresholds for alerts in the function notify_if_strong_fluctuations.<br>

Functions<br>
fetch_stock_data<br>
Fetches historical stock data for a specified ticker and period.

add_moving_average<br>
Calculates a moving average over a given window size and adds it to the data.

statistic_indicators<br>
Computes statistical measures (median, variance, max, min, etc.) for stock data.

calculate_rsi<br>
Calculates the Relative Strength Index (RSI) for the stock data.

calculate_macd<br>
Calculates the Moving Average Convergence Divergence (MACD) for the stock data.

export_to_csv<br>
Exports the data to a CSV file.

create_and_save_plot<br>
Exports the data to a HTML file.

notify_if_strong_fluctuations<br>
Checks for significant price fluctuations and triggers an alert if thresholds are exceeded.
