from InquirerPy.utils import InquirerPyStyle
from rich.console import Console
from pathlib import Path

path = Path(__file__).parent


console = Console()
colors = InquirerPyStyle({
		"question": "#00a400 bold",
		"answer": "#00a400",
		"input": "white",
		"questionmark": "#00a400 bold",
		"pointer": "#00a400"
	})


def period_spell(period):
    """
    Convert a period string to a human-readable description.

    This function takes a period code (such as '1d', '1mo', '1y') and returns its corresponding
    human-readable description. The periods correspond to various timeframes for stock data
    retrieval, and the function uses a predefined mapping to return the appropriate description.

    Args:
        period (str): The period code, e.g., '1d', '1mo', 'ytd', or 'max', representing the time period.

    Returns:
        str: A human-readable description of the period in Russian. For example, '1mo' returns '1 месяц'.
    """
    if isinstance(period, str):
        timeframes = {'1d': '1 day',
                      '5d': '5 days',
                      '1mo': '1 month',
                      '3mo': '3 months',
                      '6mo': '6 months',
                      '1y': '1 year',
                      '2y': '2 years',
                      '5y': '5 years',
                      '10y': '10 years',
                      'ytd': 'since the beginning of the current year',
                      'max': 'maximum available period'
                      }
        return timeframes[period]
    elif isinstance(period, list):
        return period[0] + '-' + period[1]