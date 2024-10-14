import yfinance as yf


def calculate_and_display_average_price(data):
    if not data.empty:
        data['MA'] = data['Close'].rolling(window=5).mean()
        print(data['MA'])


def get_quotes(ticker, period):
    stock = yf.Ticker(ticker)
    data = stock.history(period=period)
    return data


calculate_and_display_average_price(get_quotes('AAPL', '1mo'))
