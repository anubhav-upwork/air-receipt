import logging
import os
from rich.logging import RichHandler
from logging.handlers import RotatingFileHandler

x_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), "../"))
LOG_DIR = os.path.join(x_dir, "logs")
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)
LOG_FILE_PATH = os.path.join(LOG_DIR, "app.log")
LOGGING_LEVEL = logging.INFO
LOGGING_FORMAT = "%(asctime)s - %(funcName)s() - %(levelname)s - %(message)s"
logging.basicConfig(
    level=LOGGING_LEVEL, format=LOGGING_FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)  # set level=20 or logging.INFO to turn of debug

file_handler = RotatingFileHandler(LOG_FILE_PATH, maxBytes=10485760, backupCount=5)
file_handler.setLevel(LOGGING_LEVEL)
file_handler.setFormatter(logging.Formatter(LOGGING_FORMAT))
logging.getLogger("").addHandler(file_handler)
logger = logging.getLogger("rich")
