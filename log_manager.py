import logging, os
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime


class Logger:
	def __init__(self, log_dir="logs", log_level=''):
		self.log_dir = log_dir
		self.log_level = log_level

		# Logger for main with INFO level
		self.main_logger = logging.getLogger("main")
		self.main_logger.setLevel(logging.INFO)  # Main logging thread

		# Logger for functions with DEBUG level
		self.function_logger = logging.getLogger("func")
		self.function_logger.setLevel(logging.DEBUG)  # Functions' logging thread

		# Create \logs dir if it doesn't exist
		if not os.path.exists(self.log_dir):
			os.makedirs(self.log_dir)

		# Common logger settings
		log_filename = os.path.join(self.log_dir, datetime.now().strftime("%Y%m%d.log"))
		handler = TimedRotatingFileHandler(log_filename, when="midnight", interval=1)

		# Logging format: hh:mm:ss.msc\t(main or function)\tmessage
		formatter = logging.Formatter('%(asctime)s\t%(name)s\t%(message)s', datefmt='%H:%M:%S')
		handler.setFormatter(formatter)
		handler.setLevel(log_level)
		# Add handler to both loggers
		self.main_logger.addHandler(handler)
		self.function_logger.addHandler(handler)

	def get_main_logger(self):
		return self.main_logger

	def get_function_logger(self):
		return self.function_logger
