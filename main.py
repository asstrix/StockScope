from data_download import *
from data_plotting import create_and_save_plot
from log_manager import Logger, logging

logger = Logger(log_level=logging.DEBUG)  # Set INFO to exclude functions' logging


def main():
	log = logger.get_main_logger()
	func_log = logger.get_function_logger()
	log.info("Start")

	ticker = input("Enter stock ticker (e.g, «AAPL» for Apple Inc):\n")
	period = input("Enter data period (e.g, '1mo' for one month):\n")
	threshold = float(input(" Enter Enter the price fluctuation threshold: \n"))
	log.info(f"Symbol: {ticker}, Period: {period}, % fluctuation {threshold}")

	log.info(f"Getting quotes of {ticker} for {period_spell(period)}")
	stock_data = fetch_stock_data(func_log, ticker, period)

	log.info(f"Adding MA values {ticker} for {period_spell(period)}")
	add_moving_average(func_log, stock_data, 5)

	log.info(f" Adding RSI values {ticker} for {period_spell(period)}")
	calculate_rsi(func_log, stock_data)

	log.info(f"Adding MACD values {ticker} for {period_spell(period)}")
	calculate_macd(func_log, stock_data)

	log.info(f"Calculating average price for {period_spell(period)}")
	calculate_and_display_average_price(func_log, stock_data, ticker, period)

	log.info(f"Calculating % fluctuation of the average price for {period}")
	notify_if_strong_fluctuations(func_log, stock_data, threshold, ticker, period)

	log.info(f"saving average closing price chart for {period_spell(period)}")
	create_and_save_plot(func_log, stock_data, ticker, period)
	log.info(f"Saving data to csv")
	export_to_csv(func_log, stock_data, ticker, period)

	log.info("Stop")


if __name__ == "__main__":
	main()