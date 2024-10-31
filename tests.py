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

	def test_calculate_and_display_average_price_success(self):
		avg_price = cadap(self.logger, self.data, self.ticker, self.period)
		self.assertEqual(avg_price, 200.0)

	def test_nsf(self):
		threshold = 10
		result = nisf(self.logger, self.data, threshold, self.ticker, self.period)
		self.assertTrue(result)


if __name__ == '__main__':
	unittest.main()
