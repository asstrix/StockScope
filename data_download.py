import yfinance as yf


def add_moving_average(data, window_size):
    if not data.empty:
        data['MA'] = data['Close'].rolling(window=window_size).mean()
        print(data['MA'])


def fetch_stock_data(ticker, period):
    stock = yf.Ticker(ticker)
    data = stock.history(period=period)
    return data


def calculate_and_display_average_price(data):
    if not data.empty:
        average_close_price = data['Close'].mean()
        print(f'Cредняя цена закрытия акций за заданный период: {average_close_price}')