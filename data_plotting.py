import plotly.graph_objects as go
from pathlib import Path
from data_download import period_spell
import os


# Export charts as png
def create_and_save_plot(logger, data, ticker, period, theme='plotly'):
    """
        Create and save a plot of stock price data, including Close Price, Moving Average, RSI, and MACD.

        This function generates a multi-line plot using Plotly, with the stock's closing price, moving average (MA),
        Relative Strength Index (RSI), and Moving Average Convergence Divergence (MACD) displayed on different axes.
        The plot is saved as a PNG file in a 'charts' directory within the script's directory. If any directories
        do not exist, they will be created automatically. The function logs the success or failure of saving the plot.

        Args:
            logger (logging.Logger): The logger object used to log debug messages.
            data (pandas.DataFrame): A DataFrame containing stock data. It must have the columns 'Date', 'Close', 'MA',
                                     'RSI', and 'MACD'.
            ticker (str): The stock ticker symbol, which will be used in the filename.
            period (str): The period string representing the timeframe for the stock data (e.g., '1d', '1mo').
            theme (str): A theme to be applied on the chart

        Returns:
            None: The function generates and saves a plot as an image, but does not return any value.

        Logs:
            Logs a debug message when the plot is successfully saved or if an error occurs during the process.

        Raises:
            Any exceptions encountered while creating or saving the plot will be caught and logged.

        Notes:
            - The plot includes:
              - 'Close Price': displayed on the main y-axis.
              - 'Moving Average': displayed on the main y-axis.
              - 'RSI': displayed on a secondary y-axis with a range of 0 to 100.
              - 'MACD': displayed on a third y-axis overlaying the main axis.
        """
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], mode='lines', name='Close Price'))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['MA'], mode='lines', name='Moving Average'))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['RSI'], mode='lines', name='RSI', yaxis='y2'))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['MACD'], mode='lines', name='MACD', yaxis='y3'))
    fig.update_layout(
        title={'text': f"Close price for  {period_spell(period)}", 'x': 0.5, 'xanchor': 'center',
               'yanchor': 'top'},
        yaxis=dict(title='Close Price, MACD', ticklabelposition='outside left'),
        yaxis2=dict(title='RSI', overlaying='y', side='right', range=[0, 100]),
        yaxis3=dict(overlaying='y', side='left', ticklabelposition='inside'),
        width=1200,
        height=800,
        legend=dict(x=0, y=-0.25),
        template=theme
    )
    path = Path(__file__).parent
    try:
        os.makedirs(f"{path}/charts", exist_ok=True)
        fig.write_image(f"{path}/charts/{ticker}{period_spell(period)}.png")
        logger.debug(f"The chart has been saved to: {path}\\charts")
    except Exception as e:
        logger.debug(f"Error saving the chart: {e}")
