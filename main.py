from data_download import (fetch_stock_data,
                           add_moving_average,
                           calculate_rsi,
                           calculate_macd,
                           statistic_indicators,
                           calculate_and_display_average_price,
                           notify_if_strong_fluctuations,
                           export_to_csv
                           )
from tools import console, colors, period_spell
from data_plotting import create_and_save_plot
from log_manager import Logger, logging
from InquirerPy import inquirer

logger = Logger(log_level=logging.DEBUG)  # Set INFO to exclude functions' logging


def main():
	welcome_text = """
	┌────────────────────────────────────── StockScope ──────────────────────────────────────┐
	│ This tool can fetch quotes from fc.yahoo.com by builtin periods or by custom interval. │
	│     Also it adds MA, MACD, RSI and statistic indicators within close price chart.      │
	│               It is also available to export data to csv and png files.                │
	└────────────────────────────────────────────────────────────────────────────────────────┘
	"""
	console.print(f'[#00a400 bold]{welcome_text}[#00a400 bold]')
	log = logger.get_main_logger()
	func_log = logger.get_function_logger()
	log.info("Start")
	ticker = inquirer.text(message="Enter stock ticker:", instruction="e.g. «AAPL» for Apple Inc\n", style=colors).execute()
	period = inquirer.select(
		message="Select period:",
		choices=["custom", "1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd"],
		style=colors,
		cycle=False
	).execute()
	if period == "custom":
		period = [
			inquirer.text(
				message="Enter the start date (dd.mm.yyyy):",
				# validate=validate_date,
				invalid_message="Invalid date format. Please use dd.mm.yyyy.",
				style=colors
			).execute(),
			inquirer.text(
				message="Enter the end date (dd.mm.yyyy):",
				# validate=validate_date,
				invalid_message="Invalid date format. Please use dd.mm.yyyy.",
				style=colors
			).execute()
		]

	threshold = inquirer.text(message="Enter the price fluctuation threshold:", style=colors).execute()

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

	command = inquirer.text(
		message="Would you like to save data to csv?",
		instruction="y\\n\n",
		style=colors).execute()
	if command.lower() == 'y':
		log.info(f"Saving data to csv")
		export_to_csv(func_log, stock_data, ticker, period)
	command = (inquirer.text(
		message="Would you like to save data as png and html?",
		instruction="y\\n\n", style=colors).execute())
	if command.lower() == 'y':
		log.info(f"saving average closing price chart for {period_spell(period)}")
		create_and_save_plot(func_log, stock_data, ticker, period)

	log.info("Stop\n")


if __name__ == "__main__":
	main()
