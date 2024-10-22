import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from data_download import calculate_and_display_average_price as cadap
from data_download import notify_if_strong_fluctuations as nisf
from data_download import period_spell


class MathsTest(unittest.TestCase):
	data = pd.DataFrame({'Close': [100, 200, 300]})
	logger = MagicMock()
	period = '1mo'

	@patch('builtins.print')
	def test_cadap(self, mock_print):
		result = cadap(self.logger, self.data, self.period)
		mock_print.assert_called_with(f'Cредняя цена закрытия акций за {period_spell(self.period)}: 200.0')
		self.logger.debug.assert_called_with("Средняя цена закрытия вычислена")
		self.assertEqual(result, 200.0)

	@patch('builtins.print')
	def test_nsf(self, mock_print):
		threshold = 10
		result = nisf(self.logger, self.data, threshold, self.period)
		mock_print.assert_called_with(f'Колебание цены закрытия акций за {period_spell(self.period)} 200.0% превысило указанный порог 10%')
		self.assertTrue(result)


if __name__ == '__main__':
	unittest.main()
