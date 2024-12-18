import yfinance as yf
from datetime import timedelta, datetime
import os
from tools import path, console, period_spell


# Get data from fc.yahoo.com
def fetch_stock_data(logger, ticker, period):
    """
    Fetch historical stock data for a given ticker symbol over a specified period from Yahoo Finance.

    This function uses the `yfinance` library to retrieve stock price data. It logs a success message if data is obtained,
    and logs a debug message if the data could not be retrieved.

    Args:
        logger (logging.Logger): The logger object used to log debug messages.
        ticker (str): The stock ticker symbol, e.g., 'AAPL' for Apple Inc.
        period (str): The period for which to fetch the historical data.
                      Examples include '1d', '5d', '1mo', '1y', etc.

    Returns:
        pandas.DataFrame: A DataFrame containing the historical stock data, with the date as the index.
                          If no data is available, returns an empty DataFrame.

    Logs:
        Logs a debug message indicating whether the data was successfully fetched or not.
    """
    stock = yf.Ticker(ticker)
    if isinstance(period, str):
        data = stock.history(period=period).reset_index()
    if isinstance(period, list):
        start = datetime.strptime(period[0], "%d.%m.%Y")
        end = datetime.strptime(period[1], "%d.%m.%Y")
        data = stock.history(start=start - timedelta(days=1), end=end + timedelta(days=1), interval='1d').reset_index()
    if not data.empty:
        logger.debug(f"Quotes for symbol {ticker} received successfully")
        return data
    else:
        logger.debug(f"Quotes for symbol {ticker} not received")


# Calculate moving average based on close prices
def add_moving_average(logger, data, window_size):
    """
    Add a moving average (MA) column to the stock data over a specified window size.

    This function calculates the moving average of the 'Close' prices in the input DataFrame and adds it as a new column
    named 'MA'. If an error occurs during the calculation or adding the column, an exception is caught, and a debug
    message is logged.

    Args:
        logger (logging.Logger): The logger object used to log debug messages.
        data (pandas.DataFrame): A DataFrame containing stock data, which must have a 'Close' column with price data.
        window_size (int): The window size (in days) over which to compute the moving average.

    Returns:
        None: This function modifies the input DataFrame in place, adding a new column 'MA' with the calculated moving averages.

    Logs:
        Logs a debug message if the moving average column was successfully added or if an error occurred during the process.
    """
    try:
        data['MA'] = data['Close'].rolling(window=window_size).mean()
        logger.debug(f"Column with moving average price for {window_size} days added")
    except Exception as e:
        logger.debug(f"Moving average price column not added: {e}")


# Calculate statistic indicators
def statistic_indicators(logger, data, ticker, period):
    """
    Calculates key statistical indicators for a dataset of closing prices and updates the 'data' dictionary with results.

    This function computes the median, standard deviation (STD), variance, maximum, minimum, and coefficient of variation
    for the 'Close' column in the provided dataset and stores these indicators in the 'data' dictionary. The function also
    logs the completion of the calculation or any errors encountered.

   Args:
        logger (logging.Logger): The logger object used to log debug messages.
        data (pandas.DataFrame): A DataFrame containing stock data, which must have a 'Close' column with price data.
        ticker (str): The stock ticker symbol (e.g., 'AAPL').
        period (str): A string representing the time period for which the average price is calculated
                      (e.g., '1d', '1mo').

    Returns:
        None

    Logs:
        Logs a debug message when the statistic indicators are successfully calculated or if an error occurs.

    """
    try:
        data['Median'] = data['Close'].median()
        data['STD'] = data['Close'].std()
        data['Variance'] = data['Close'].var()
        data['Max'] = data['Close'].max()
        data['Min'] = data['Close'].min()
        data['Var_coef'] = (data['Close'].std() / data['Close'].mean()) * 100
        logger.debug(f"Statistic indicators have been calculated")
    except Exception as e:
        logger.debug(f"Error calculating statistic indicators: {e}")


# Average price for whole requested period
def calculate_and_display_average_price(logger, data, ticker, period):
    """
    Calculate and display the average closing price of a stock for a given period.

    This function computes the average closing price from the 'Close' column in the provided DataFrame.
    It prints the result to the console and logs a debug message. If an error occurs during the calculation,
    the error is caught, logged, and the function continues execution.

    Args:
        logger (logging.Logger): The logger object used to log debug messages.
        data (pandas.DataFrame): A DataFrame containing stock data with a 'Close' column.
        ticker (str): The stock ticker symbol (e.g., 'AAPL').
        period (str): A string representing the time period for which the average price is calculated
                      (e.g., '1d', '1mo').

    Returns:
        float: The calculated average closing price. Returns None if an exception occurs.

    Logs:
        Logs a debug message when the average price is successfully calculated or if an error occurs.

    Prints:
        Outputs the average closing price of the specified stock and period in a formatted string to the console.
    """
    try:
        avg_price = data['Close'].mean()
        logger.debug(f"Average closing price calculated")
        console.print(f'[#00a400 bold]Average closing price of {ticker} for {period_spell(period)}: {avg_price}[#00a400 bold]')
        return avg_price
    except Exception as e:
        logger.debug(f"Error calculating average closing price: {e}")


# Print an alert if fluctuation exceeded expectations
def notify_if_strong_fluctuations(logger, data, threshold, ticker, period):
    """
    Calculate and display the average closing price of stocks for a given period.

    This function computes the average closing price from the 'Close' column in the input DataFrame and displays the result
    in a formatted string using the specified period. It also logs the success or failure of the calculation.

    Args:
        logger (logging.Logger): The logger object used to log debug messages.
        data (pandas.DataFrame): A DataFrame containing stock data, which must have a 'Close' column with price data.
        threshold (float): User specified threshold.
        ticker (str): User specified symbol.
        period (str): A string representing the period over which the average price is being calculated, e.g., '1mo', '1y'.

    Returns:
        float: The calculated average closing price of the stock.
               If an error occurs, the function returns None.

    Logs:
        Logs a debug message when the average price is successfully calculated or if an error occurs during the process.

    Prints:
        Outputs the average closing price in a formatted string that includes the human-readable version of the period,
        which is determined by the `period_spell` function.
    """
    try:
        fluctuation = ((data['Close'].max() - data['Close'].min()) / data['Close'].min()) * 100
        if fluctuation > threshold:
            console.print(f'[#00a400 bold]The fluctuation in the closing price of {ticker}\
             for {period_spell(period)} {fluctuation}% exceeded the specified threshold {threshold}%\n[#00a400 bold]')
            logger.debug(f"% fluctuation in closing price calculated successfully")
            return True
        return False
    except Exception as e:
        logger.debug(f"Error calculating the closing price fluctuation: {e}")


# Export all fetched data to csv
def export_to_csv(logger, data, ticker, period):
    """
    Export stock data to a CSV file, creating necessary directories if they do not exist.

    This function exports the provided DataFrame to a CSV file. The file is saved in a 'csv' directory
    within the script's directory. The filename includes the stock ticker and the period. If any directories
    in the path do not exist, they will be created automatically. The function logs the success or failure of the export.

    Args:
        logger (logging.Logger): The logger object used to log debug messages.
        data (pandas.DataFrame): The DataFrame containing the stock data to be exported.
        ticker (str): The stock ticker symbol, which will be included in the filename.
        period (str): The period string, which will also be part of the filename (e.g., '1d', '1mo').

    Returns:
        None: This function performs an export to CSV and logs messages. It does not return any value.

    Logs:
        Logs a debug message when the data is successfully saved to CSV or if an error occurs during the export process.

    Raises:
        Any exceptions encountered during the file export will be caught and logged.
    """
    os.makedirs(f"{path}/csv", exist_ok=True)
    try:
        data.to_csv(f"{path}/csv/{ticker}{period_spell(period)}.csv")
        logger.debug(f"Data saved in: {path}\\csv\\{ticker}{period_spell(period)}.csv")
        console.print(f"[#00a400 bold]Data saved in: {path}\\csv\\{ticker}{period_spell(period)}.csv[#00a400 bold]")
    except Exception as e:
        logger.debug(f"Error saving data: {e}")


# Calculate RSI with default 14 period
def calculate_rsi(logger, data):
    """
   Calculate the Relative Strength Index (RSI) for stock price data and add it as a new column to the DataFrame.

   The RSI is a momentum indicator that measures the magnitude of recent price changes to evaluate overbought or
   oversold conditions in the stock price. This function computes the RSI using a 14-period rolling window and
   appends the result as a new column named 'RSI' in the provided DataFrame. The function logs the success or
   failure of this operation.

   Args:
       logger (logging.Logger): The logger object used to log debug messages.
       data (pandas.DataFrame): A DataFrame containing stock data, which must have a 'Close' column with price data.

   Returns:
       None: This function modifies the input DataFrame in place, adding a new column 'RSI' with the calculated RSI values.

   Logs:
       Logs a debug message when the RSI column is successfully added or if an error occurs during the calculation.

   Raises:
       Any exceptions encountered during the calculation will be caught and logged.
   """
    try:
        # Difference between current and previous close price
        delta = data['Close'].diff()

        # Positive and negative changes
        gain = delta.where(delta > 0, 0)  # Only positive changes
        loss = -delta.where(delta < 0, 0)  # Only negative changes (abs values)

        # Average values
        avg_gain = gain.rolling(window=14, min_periods=1).mean()
        avg_loss = loss.rolling(window=14, min_periods=1).mean()

        # Relative Strength
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        data['RSI'] = rsi
        logger.debug(f"RSI column has been added")
    except Exception as e:
        logger.debug(f"RSI column not added: {e}")


# Calculate macd with default short=12 and long=26 periods
def calculate_macd(logger, data):
    """
    Calculate the Moving Average Convergence Divergence (MACD) for stock price data and add it as a new column to the DataFrame.

    MACD is a trend-following momentum indicator that shows the relationship between two moving averages of a stock's price.
    This function computes the MACD as the difference between the 12-period exponential moving average (EMA) and the
    26-period EMA, and appends the result as a new column named 'MACD' in the provided DataFrame. The function logs the
    success or failure of the calculation.

    Args:
        logger (logging.Logger): The logger object used to log debug messages.
        data (pandas.DataFrame): A DataFrame containing stock data, which must have a 'Close' column with price data.

    Returns:
        None: This function modifies the input DataFrame in place, adding a new column 'MACD' with the calculated MACD values.

    Logs:
        Logs a debug message when the MACD column is successfully added or if an error occurs during the calculation.

    Raises:
        Any exceptions encountered during the calculation will be caught and logged.
    """
    try:
        short_ema = data['Close'].ewm(span=12, adjust=False).mean()
        long_ema = data['Close'].ewm(span=26, adjust=False).mean()
        data['MACD'] = short_ema - long_ema
        logger.debug(f"MACD column has been added")
    except Exception as e:
        logger.debug(f"MACD column not added: {e}")
