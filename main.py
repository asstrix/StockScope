from data_download import fetch_stock_data, calculate_and_display_average_price, notify_if_strong_fluctuations, export_to_csv
from log_manager import Logger, logging

logger = Logger(log_level=logging.DEBUG)  # Set INFO to exclude functions' logging


def main():
	log = logger.get_main_logger()
	func_log = logger.get_function_logger()
	log.info("Старт")

	ticker = input("Введите тикер акции (например, «AAPL» для Apple Inc):\n")
	period = input("Введите период для данных (например, '1mo' для одного месяца):\n")
	threshold = float(input("Введите порог колебания цены в %: \n"))
	log.info(f"Символ: {ticker}, Период: {period}, % колебания {threshold}")

	log.info(f"Получаем котировки по символу {ticker} за {period}")
	stock_data = fetch_stock_data(func_log, ticker, period)

	log.info(f"Рассчитываем среднюю цену закрытия за весь период")
	calculate_and_display_average_price(func_log, stock_data)

	log.info(f"Рассчитываем % колебания средней цены за период")
	notify_if_strong_fluctuations(func_log, stock_data, threshold)

	log.info(f"Сохраняем данные в csv")
	export_to_csv(func_log, stock_data, f'{ticker}{period}')

	log.info("Стоп")


if __name__ == "__main__":
	main()