from data_download import *
from data_plotting import create_and_save_plot
from log_manager import Logger, logging
from datetime import datetime
from pathlib import Path

logger = Logger(log_level=logging.DEBUG)  # Set INFO to exclude functions' logging


def main():
	path = Path(__file__).parent
	log = logger.get_main_logger()
	func_log = logger.get_function_logger()
	log.info("Start")

	ticker = input("Enter stock ticker (e.g, «AAPL» for Apple Inc):\n")
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

	log.info(f"Calculating average price for {period_spell(period)}")
	calculate_and_display_average_price(func_log, stock_data, ticker, period)

	log.info(f"Calculating % fluctuation of the average price for {period_spell(period)}")
	notify_if_strong_fluctuations(func_log, stock_data, threshold, ticker, period)

	command = input('Would you like to save data to csv? y\\n\n')
	if command == 'y':
		log.info(f"Saving data to csv")
		export_to_csv(func_log, stock_data, ticker, period)
		print(f"Data saved in: {path}\\csv\\{ticker}{period_spell(period)}.csv")
	command = input('Would you like to save chart as png? y\\n\n')
	if command == 'y':
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
			create_and_save_plot(func_log, stock_data, ticker, period, themes[choice])
		else:
			create_and_save_plot(func_log, stock_data, ticker, period)
		log.info(f"saving average closing price chart for {period_spell(period)}")
		print(f"The chart has been saved to: {path}\\charts\\{ticker}{period_spell(period)}.png")
	log.info("Stop")


if __name__ == "__main__":
	main()