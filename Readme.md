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
- [Contributing](#contributing)
- [License](#license)

## Features

- **Fetch stock data** for specified tickers and periods using Yahoo Finance.
- **Calculate statistical indicators** such as mean, variance, and standard deviation of stock prices.
- **Add financial indicators** like Moving Average (MA), MACD, and RSI to the data.
- **Export data to CSV** for offline analysis.
- **Threshold-based alerts** for price fluctuations.
- **Console output** with human-readable descriptions of the analysis results.

## Installation

To run StockScope, you need Python 3.x and the required packages. Clone this repository and install dependencies:

bash
git clone https://github.com/asstrix/StockScope.git
cd StockScope
pip install -r requirements.txt


Usage
Initialize the Logger: Set up logging to track program actions.
Specify Ticker and Period: Input the stock ticker and desired period (e.g., 'AAPL' and '1mo').
Call Functions: Use functions such as fetch_stock_data, add_moving_average, or calculate_rsi to analyze the data.
Export Results: Export data to a CSV file with export_to_csv.
Example Code
python
Copy code
import logging
from data_download import fetch_stock_data, add_moving_average, export_to_csv

# Initialize logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

# Fetch data
data = fetch_stock_data(logger, ticker="AAPL", period="1mo")

# Add moving average
add_moving_average(logger, data, window_size=20)

# Export to CSV
export_to_csv(logger, data, ticker="AAPL", period="1mo")
Configuration
Adjust settings as needed:

Period codes: Adjusted with period_spell function for custom periods like '1d', '1mo', or date ranges.
Logger: Configure logging level and format in the main script for additional debugging.
Thresholds: Define price fluctuation thresholds for alerts in the function notify_if_strong_fluctuations.
Functions
fetch_stock_data
Fetches historical stock data for a specified ticker and period.

add_moving_average
Calculates a moving average over a given window size and adds it to the data.

statistic_indicators
Computes statistical measures (median, variance, max, min, etc.) for stock data.

calculate_rsi
Calculates the Relative Strength Index (RSI) for the stock data.

calculate_macd
Calculates the Moving Average Convergence Divergence (MACD) for the stock data.

export_to_csv
Exports the data to a CSV file.

notify_if_strong_fluctuations
Checks for significant price fluctuations and triggers an alert if thresholds are exceeded.
