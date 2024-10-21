from data_download import *
from data_plotting import create_and_save_plot
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

	log.info(f"Получаем котировки по символу {ticker} за {period_spell(period)}")
	stock_data = fetch_stock_data(func_log, ticker, period)

	log.info(f"Добавляем значения MA {ticker} за {period_spell(period)}")
	add_moving_average(func_log, stock_data, 5)

	log.info(f"Рассчитываем среднюю цену закрытия за {period_spell(period)}")
	calculate_and_display_average_price(func_log, stock_data, period)

	log.info(f"Рассчитываем % колебания средней цены за период")
	notify_if_strong_fluctuations(func_log, stock_data, threshold, period)

	log.info(f"Сохраняем график средней цены закрытия за {period_spell(period)}")
	create_and_save_plot(func_log, stock_data, ticker, period)
	log.info(f"Сохраняем данные в csv")
	export_to_csv(func_log, stock_data, ticker, period)

	log.info("Стоп")


if __name__ == "__main__":
	main()