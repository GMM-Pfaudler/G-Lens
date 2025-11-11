import logging
import os
from datetime import datetime

# -----------------------------------------------------
# 🔧 Setup: Create logs directory
# -----------------------------------------------------
LOG_DIR = os.path.join(os.getcwd(), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# Common formatter
FORMATTER = logging.Formatter(
    "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Cache current file info
_current_date = datetime.now().strftime("%Y-%m-%d")
_current_log_file = os.path.join(LOG_DIR, f"{_current_date}.log")


# -----------------------------------------------------
# 🧱 Logger Factory
# -----------------------------------------------------
def get_logger(module_name: str) -> logging.Logger:
    """
    Returns a logger for the given module.
    Automatically switches to a new date-based file when the date changes.
    """
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.INFO)

    global _current_date, _current_log_file

    # Check if the date changed (new day)
    today = datetime.now().strftime("%Y-%m-%d")
    if today != _current_date:
        _current_date = today
        _current_log_file = os.path.join(LOG_DIR, f"{today}.log")

        # Close and remove old file handlers
        for handler in list(logger.handlers):
            if isinstance(handler, logging.FileHandler):
                handler.close()
                logger.removeHandler(handler)

    # If logger has no file handler (new process or new date)
    if not any(isinstance(h, logging.FileHandler) for h in logger.handlers):
        file_handler = logging.FileHandler(_current_log_file, mode="a", encoding="utf-8")
        file_handler.setFormatter(FORMATTER)
        logger.addHandler(file_handler)

    # Add console handler only once
    if not any(isinstance(h, logging.StreamHandler) for h in logger.handlers):
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(FORMATTER)
        logger.addHandler(console_handler)

    return logger


# -----------------------------------------------------
# ✨ Simple event logger
# -----------------------------------------------------
def log_event(module: str, level: str, message: str):
    """
    Logs an event message with the specified level.
    Level can be: info | warning | error | success | debug
    """
    logger = get_logger(module)
    level = level.lower().strip()

    if level == "info":
        logger.info(message)
    elif level == "warning":
        logger.warning(message)
    elif level == "error":
        logger.error(message)
    elif level == "success":
        logger.info(f"[SUCCESS] {message}")
    elif level == "debug":
        logger.debug(message)
    elif level == "started":
        logger.info(f"[STARTED] {message}")
    elif level == "completed":
        logger.info(f"[COMPLETED] {message}")
    else:
        logger.info(message)
