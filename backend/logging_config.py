import logging
from logging.handlers import RotatingFileHandler
import os


# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

# Log format
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s - %(message)s"

# Error log file handler: 5 MB per file, keep 5 backups
error_file_handler = RotatingFileHandler(
    filename="logs/error.log",
    maxBytes=5 * 1024 * 1024, # 5 MB
    backupCount=5,
    encoding="utf-8",
)
error_file_handler.setFormatter(logging.Formatter(LOG_FORMAT))

# Access log file handler: 5 MB per file, keep 5 backups
access_file_handler = RotatingFileHandler(
    filename="logs/access.log",
    maxBytes=5 * 1024 * 1024, # 5 MB
    backupCount=5,
    encoding="utf-8",
)
access_file_handler.setFormatter(logging.Formatter(LOG_FORMAT))

console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter(LOG_FORMAT))

# Configure root logger to avoid conflicts
logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    handlers=[],
)

# Custom loggers
app_error_logger = logging.getLogger("app.error")
app_error_logger.setLevel(logging.INFO)
app_error_logger.addHandler(error_file_handler)
app_error_logger.addHandler(console_handler)
app_error_logger.propagate = False  # Prevent propagation to avoid conflicts

app_access_logger = logging.getLogger("app.access")
app_access_logger.setLevel(logging.INFO)
app_access_logger.addHandler(access_file_handler)
app_access_logger.addHandler(console_handler)
app_access_logger.propagate = False  # Prevent propagation to avoid conflicts


def get_error_logger():
    return app_error_logger


def get_access_logger():
    return app_access_logger
