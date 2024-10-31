import plotly.graph_objects as go
from pathlib import Path
from data_download import period_spell
import os


# Export charts as png
def create_and_save_plot(logger, data, ticker, period):
    """
        Create and save a plot of stock price data, including Close Price, Moving Average, RSI, and MACD.

        This function generates a multi-line plot using Plotly, with the stock's closing price, moving average (MA),
        Relative Strength Index (RSI), and Moving Average Convergence Divergence (MACD), Median, Standard Deviation,
        Variance, Max and Min Close price values and Coefficient of Variation are displayed on different axes
        with selected theme, if no theme is selected the chart builds by default theme.
        The plot is saved as an interactive chart in html format in the 'charts' directory within the script's directory.
        If any directories do not exist, they will be created automatically. The function logs the success or failure of
        saving the plot.

        Args:
            logger (logging.Logger): The logger object used to log debug messages.
            data (pandas.DataFrame): A DataFrame containing stock data. It must have the columns 'Date', 'Close', 'MA',
                                     'RSI', and 'MACD', 'Median', 'STD', 'Variance', 'Max', 'Min', 'Var_coef'.
            ticker (str): The stock ticker symbol, which will be used in the filename.
            period (str): The period string representing the timeframe for the stock data (e.g., '1d', '1mo').

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
              - 'Max Min': displayed maximum and minimum close price values.
              - 'Median': displayed middle of close price series.
              - 'STD': Standard deviation, displayed measure of volatility.
              - 'Variance': displayed close price spread around the average.
              - 'Coefficient of Variation': displayed ratio of standard deviation to mean
        """
    themes = {
        '1': 'plotly_white', '2': 'plotly_dark',
        '3': 'ggplot2', '4': 'seaborn', '5': 'simple_white',
        '6': 'presentation', '7': 'xgridoff', '8': 'ygridoff',
        '9': 'gridon', '10': 'polar'
    }
    command = input('Would you like to change a theme? y\\n\n')
    if command == 'y':
        choice = input(
            'Please select one of available themes:\n' +
            "\n".join(f"{i + 1}. {j}" for i, j in enumerate(themes.values())) + "\n"
        )
        theme = themes[choice]
    else:
        theme = 'plotly'
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], mode='lines', name='Close Price'))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['MA'], mode='lines', name='Moving Average'))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['RSI'], mode='lines', name='RSI', yaxis='y2'))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['MACD'], mode='lines', name='MACD', yaxis='y3'))

    fig.add_trace(go.Scatter(x=data['Date'], y=data['Median'], mode='lines', name='Median'))
    fig.add_trace(
        go.Scatter(x=data['Date'], y=data['STD'], mode='lines', name='Standard Deviation', yaxis='y4'))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Variance'], mode='lines', name='Variance', yaxis='y5'))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Max'], mode='lines', name='Max'))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Min'], mode='lines', name='Min'))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Var_coef'], mode='lines', name='Coefficient of Variation', yaxis='y6'))

    fig.update_layout(
        title={'text': f"Close price for  {period_spell(period)}", 'x': 0.5, 'xanchor': 'center',
               'yanchor': 'top'},
        yaxis=dict(title='Close Price, MACD', ticklabelposition='outside left'),
        yaxis2=dict(title='RSI', overlaying='y', side='right', range=[0, 100]),
        yaxis3=dict(overlaying='y', side='left', ticklabelposition='inside'),
        yaxis4=dict(overlaying='y', range=[min(data['STD']), max(data['STD'])], showticklabels=False, visible=False),
        yaxis5=dict(overlaying='y', range=[min(data['Variance']), max(data['Variance'])], showticklabels=False, visible=False),
        yaxis6=dict(overlaying='y', range=[min(data['Var_coef']), max(data['Var_coef'])], showticklabels=False,
                    visible=False),
        width=1920,
        height=1080,
        legend=dict(x=0, y=-0.5),
        template=theme
    )
    path = Path(__file__).parent
    try:
        os.makedirs(f"{path}/charts", exist_ok=True)
        fig.write_html(f"{path}/charts/{ticker}{period_spell(period)}.html")
        logger.debug(f"The chart has been saved to: {path}\\charts\\{ticker}{period_spell(period)}.html")
        print(f"The chart has been saved to: {path}\\charts\\{ticker}{period_spell(period)}.html")
        fig.write_image(f"{path}/charts/{ticker}{period_spell(period)}.png")
        logger.debug(f"The chart has been saved to: {path}\\charts\\{ticker}{period_spell(period)}.png")
        print(f"The chart has been saved to: {path}\\charts\\{ticker}{period_spell(period)}.png")
    except Exception as e:
        logger.debug(f"Error saving the chart: {e}")
