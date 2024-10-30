from InquirerPy import inquirer
from InquirerPy.utils import InquirerPyStyle
from rich.console import Console


console = Console()
colors = InquirerPyStyle({
	"question": "#00a400 bold",
	"answer": "#00a400",
	"input": "white",
	"questionmark": "#00a400 bold",
	"pointer": "#00a400"
})
welcome_text = """
┌────────────────────────────────────── StockScope ──────────────────────────────────────┐
│ This tool can fetch quotes from fc.yahoo.com by builtin periods or by custom interval. │
│     Also it adds MA, MACD, RSI and statistic indicators within close price chart.      │
│               It is also available to export data to csv and png files.                │
└────────────────────────────────────────────────────────────────────────────────────────┘
"""
console.print(f'[#00a400 bold]{welcome_text}[#00a400 bold]')
ticker = inquirer.text(message="Enter stock ticker:", instruction="e.g. «AAPL» for Apple Inc\n", style=colors).execute()
period = inquirer.select(
	message="Select period:",
	choices=["custom", "1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd"],
	style=colors,
	cycle=False
).execute()
if period == "custom":
	start_date = inquirer.text(
		message="Enter the start date (dd.mm.yyyy):",
		# validate=validate_date,
		invalid_message="Invalid date format. Please use dd.mm.yyyy.",
		style=colors
	).execute()
	end_date = inquirer.text(
		message="Enter the end date (dd.mm.yyyy):",
		# validate=validate_date,
		invalid_message="Invalid date format. Please use dd.mm.yyyy.",
		style=colors
	).execute()

threshold = inquirer.text(message="Enter the price fluctuation threshold:", style=colors).execute()
