import logging
import os
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime

def setup_logging():
    """
    Configures the Global Logger to write to daily files.
    Structure: logs/YYYY-MM-DD.log
    """
    # Create logs directory if not exists
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Base logger
    logger = logging.getLogger("fastapi_app")
    logger.setLevel(logging.INFO)

    # Format
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Handler: Daily Rotation
    # filename will be the prefix, usually appended with current date by the handler
    # But TimedRotatingFileHandler appends suffix automatically.
    # To get precise "YYYY-MM-DD.log" naming requires some customization or 
    # relying on the default suffixing "app.log.YYYY-MM-DD".
    # Let's use a standard "app.log" that rotates.
    
    file_handler = TimedRotatingFileHandler(
        filename=os.path.join(log_dir, "app.log"),
        when="midnight",
        interval=1,
        backupCount=30, # Keep 30 days
        encoding="utf-8"
    )
    file_handler.suffix = "%Y-%m-%d"
    file_handler.setFormatter(formatter)
    
    # Console Handler (so we still see output in terminal)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

# Singleton instance
logger = setup_logging()
