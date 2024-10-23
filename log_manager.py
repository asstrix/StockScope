import logging, os
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime


class Logger:
	"""
	A custom logging class that sets up logging for both the main process and individual functions.

	The Logger class creates two loggers:
	- `main_logger`: Used for logging general information at the INFO level.
	- `function_logger`: Used for logging detailed debug information at the DEBUG level.

	Log files are stored in a specified directory (default is "logs") and are rotated daily at midnight.
	Both loggers share the same logging format and settings, with log messages stored in a time-stamped file.

	Attributes:
		log_dir (str): Directory where log files will be saved. Defaults to "logs".
		log_level (str): The log level for the file handler, controls which messages are recorded in the file.
		main_logger (logging.Logger): Logger for main processes, logs at INFO level.
		function_logger (logging.Logger): Logger for function-level debugging, logs at DEBUG level.

	Methods:
		__init__(log_dir="logs", log_level=''):
			Initializes the logger class with the specified logging directory and log level,
			and sets up the loggers and file handlers.

		get_main_logger():
			Returns the logger used for main process logging, which logs messages at the INFO level.

		get_function_logger(self):
			Returns the logger used for function-level logging, which logs messages at the DEBUG level.
	"""
	def __init__(self, log_dir="logs", log_level=logging.INFO):
		"""
		Initialize the Logger class, setting up loggers and file handlers.

		Args:
			log_dir (str): Directory where log files will be stored. Defaults to "logs".
			log_level (str): The log level for the file handler. Defaults to the level set for individual loggers.

		Functionality:
			- Creates a logging directory if it does not exist.
			- Sets up two loggers: one for general logging (`main_logger`) and one for function-level logging (`function_logger`).
			- Configures a TimedRotatingFileHandler to rotate logs daily at midnight.
			- Applies a consistent logging format for both loggers.
		"""
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
		handler = TimedRotatingFileHandler(log_filename, when="midnight", interval=1, encoding='utf-8')

		# Logging format: hh:mm:ss.msc\t(main or function)\tmessage
		formatter = logging.Formatter(fmt='%(asctime)s.%(msecs)03d\t%(name)s\t%(message)s', datefmt='%H:%M:%S')
		handler.setFormatter(formatter)
		handler.setLevel(log_level)
		# Add handler to both loggers
		self.main_logger.addHandler(handler)
		self.function_logger.addHandler(handler)

	def get_main_logger(self):
		"""
		Get the main logger instance.

		This method returns the logger used for main process logging, which logs messages at the INFO level.

		Returns:
			logging.Logger: The logger instance for main process logging.
		"""
		return self.main_logger

	def get_function_logger(self):
		"""
		Get the function-level logger instance.

		This method returns the logger used for function-level logging, which logs messages at the DEBUG level.

		Returns:
			logging.Logger: The logger instance for function-level debugging.
		"""
		return self.function_logger
