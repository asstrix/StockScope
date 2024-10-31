from data_download import *
from data_plotting import create_and_save_plot
from log_manager import Logger, logging
from datetime import datetime

logger = Logger(log_level=logging.DEBUG)  # Set INFO to exclude functions' logging


def main():
	width = 80
	text = """
		Welcome to StockScope
		This tool can fetch quotes from fc.yahoo.com by builtin periods or by custom interval.
		Also it adds MA, MACD, RSI indicators within Close prices chart.
		It is also available to export data to csv and png files.\n
		"""
	example = """Period examples:
				builtin: 1d - 1 day, 5d - 5 days, 1mo - 1 month, 3mo - 3 month, 6mo - 6 month, 1y - 1 year, 2y - 2 years,
						 5y - 5 years, 10y - 10 years, ytd - since the beginning of the current year, max: maximum available period
				custom:
						 start date - 01.01.1970
						 end date - 10.01.1970
	    """
	print("".join(line.center(width) + "\n" for line in text.strip().splitlines()))
	log = logger.get_main_logger()
	func_log = logger.get_function_logger()
	log.info("Start")
	ticker = input("Enter stock ticker (e.g, «AAPL» for Apple Inc):\n")
	print(example)
	period = input("Enter data period (e.g, '1mo' for one month, 'custom' for custom period):\n")
	if period == 'custom':
		start = datetime.strptime(input("Enter start date in dd.mm.yyyy format:\n"), "%d.%m.%Y")
		end = datetime.strptime(input("Enter end date in dd.mm.yyyy format:\n"), "%d.%m.%Y")
		period = [start, end]
	threshold = float(input("Enter the price fluctuation threshold: \n"))
	log.info(f"Symbol: {ticker}, Period: {period_spell(period)}, % fluctuation {threshold}")

	log.info(f"Getting quotes of {ticker} for {period_spell(period)}")
	stock_data = fetch_stock_data(func_log, ticker, period)

	log.info(f"Adding MA values {ticker} for {period_spell(period)}")
	add_moving_average(func_log, stock_data, 5)

	log.info(f" Adding RSI values {ticker} for {period_spell(period)}")
	calculate_rsi(func_log, stock_data)

	log.info(f"Adding MACD values {ticker} for {period_spell(period)}")
	calculate_macd(func_log, stock_data)

	log.info(f"Adding statistic indicators {ticker} for {period_spell(period)}")
	statistic_indicators(func_log, stock_data, ticker, period)

	log.info(f"Calculating average price for {period_spell(period)}")
	calculate_and_display_average_price(func_log, stock_data, ticker, period)

	log.info(f"Calculating % fluctuation of the average price for {period_spell(period)}")
	notify_if_strong_fluctuations(func_log, stock_data, threshold, ticker, period)

	command = input('Would you like to save data to csv? y\\n\n')
	if command.lower() == 'y':
		log.info(f"Saving data to csv")
		export_to_csv(func_log, stock_data, ticker, period)
	command = input('Would you like to save data as png and html? y\\n\n')
	if command.lower() == 'y':
		log.info(f"saving average closing price chart for {period_spell(period)}")
		create_and_save_plot(func_log, stock_data, ticker, period)

	log.info("Stop\n")


if __name__ == "__main__":
	main()