from data_download import *


def main():
	ticker = input("Введите тикер акции (например, «AAPL» для Apple Inc):\n")
	period = input("Введите период для данных (например, '1mo' для одного месяца):\n")
	stock_data = fetch_stock_data(ticker, period)
	calculate_and_display_average_price(stock_data)


if __name__ == "__main__":
	main()