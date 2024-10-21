import yfinance as yf
from pathlib import Path


# Get data from fc.yahoo.com
def fetch_stock_data(logger, ticker, period):
    stock = yf.Ticker(ticker)
    data = stock.history(period=period).reset_index()
    if not data.empty:
        logger.debug(f"Котировки по символу {ticker} получены успешно")
        return data
    else:
        logger.debug(f"Котировки по символу {ticker} не получены")


# Calculate moving average based on close prices
def add_moving_average(logger, data, window_size):
    try:
        data['MA'] = data['Close'].rolling(window=window_size).mean()
        logger.debug(f"Колонка со средней ценой за {window_size} дней добавлена")
    except Exception as e:
        logger.debug(f"Колонка со средней ценой не добавлена: {e}")


# Average price for whole requested period
def calculate_and_display_average_price(logger, data, period):
    try:
        average_close_price = data['Close'].mean()
        print(f'Cредняя цена закрытия акций за {period_spell(period)}: {average_close_price}')
        logger.debug(f"Средняя цена закрытия вычислена")
        return average_close_price
    except Exception as e:
        logger.debug(f"Ошибка вычисления средней цены закрытия: {e}")


# Print an alert if fluctuation exceeded expectations
def notify_if_strong_fluctuations(logger, data, threshold, period):
    try:
        fluctuation = ((data['Close'].max() - data['Close'].min()) / data['Close'].min()) * 100
        if fluctuation > threshold:
            print(f'Колебание цены закрытия акций за {period_spell(period)} {fluctuation}% превысило указанный порог {threshold}%')
            logger.debug(f"% колебания цены закрытия рассчитан успешно")
            return True
        return False
    except Exception as e:
        logger.debug(f"Ошибка вычисления колебания цены закрытия: {e}")


# Export all fetched data to csv
def export_to_csv(logger, data, filename):
    path = Path(__file__).parent
    try:
        data.to_csv(filename)
        logger.debug(f"Данные сохранены в: {path}\\{filename}.csv")
    except Exception as e:
        logger.debug(f"Ошибка вычисления колебания цены закрытия: {e}")


def period_spell(period):
    timeframes = {'1d': '1 день',
                  '5d': '5 дней',
                  '1mo': '1 месяц',
                  '3mo': '3 месяца',
                  '6mo': 'полгода',
                  '1y': '1 год',
                  '2y': '2 года',
                  '5y': '5 лет',
                  '10y': '10 лет',
                  'ytd': 'с начала текущего года',
                  'max': f'максимальный доступный период'
                  }
    return timeframes[period]