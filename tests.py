import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from data_download import calculate_and_display_average_price as cadap
from data_download import notify_if_strong_fluctuations as nisf


class MathsTest(unittest.TestCase):
	data = pd.DataFrame({'Close': [100, 200, 300]})
	logger = MagicMock()
	ticker = 'AAPL'
	period = '1mo'

	@patch('builtins.print')
	def test_cadap(self, mock_print):
		result = cadap(self.logger, self.data, self.ticker,  self.period)
		mock_print.assert_called_with(f'Average closing price of AAPL for 1 month: 200.0')
		self.logger.debug.assert_called_with("Average closing price calculated")
		self.assertEqual(result, 200.0)

	@patch('builtins.print')
	def test_nsf(self, mock_print):
		threshold = 10
		result = nisf(self.logger, self.data, threshold, self.ticker, self.period)
		mock_print.assert_called_with(
			f'The fluctuation in the closing price of AAPL for 1 month 200.0% exceeded the specified threshold 10%\n'
		)
		self.assertTrue(result)


if __name__ == '__main__':
	unittest.main()
