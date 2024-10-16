import yfinance as yf


# Get data from fc.yahoo.com
def fetch_stock_data(logger, ticker, period):
    stock = yf.Ticker(ticker)
    data = stock.history(period=period)
    if not data.empty:
        logger.debug(f"Котировки по символу {ticker} получены успешно")
        return data
    else:
        logger.debug(f"Котировки по символу {ticker} не получены")


# Calculate moving average based on close prices
def add_moving_average(logger, data, window_size):
    try:
        data['MA'] = data['Close'].rolling(window=window_size).mean()
        print(data['MA'])
        logger.debug(f"Колонка со средней ценой добавлена")
    except Exception as e:
        logger.debug(f"Колонка со средней ценой не добавлена: {e}")


# Average price for whole requested period
def calculate_and_display_average_price(logger, data):
    try:
        average_close_price = data['Close'].mean()
        print(f'Cредняя цена закрытия акций за заданный период: {average_close_price}')
        logger.debug(f"Средняя цена закрытия вычислена")
        return average_close_price
    except Exception as e:
        logger.debug(f"Ошибка вычисления средней цены закрытия: {e}")


# Print an alert if fluctuation exceeded expectations
def notify_if_strong_fluctuations(logger, data, threshold):
    try:
        fluctuation = ((data['Close'].max() - data['Close'].min()) / data['Close'].min()) * 100
        if fluctuation > threshold:
            print(f'Колебание цены закрытия акций за заданный период {fluctuation}% превысило указанный порог {threshold}%')
            logger.debug(f"% колебания цены закрытия рассчитан успешно")
            return True
        return False
    except Exception as e:
        logger.debug(f"Ошибка вычисления колебания цены закрытия: {e}")