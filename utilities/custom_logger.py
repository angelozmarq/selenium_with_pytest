import logging
import sys
import os
from datetime import datetime

def custom_logger(name: str, log_path: str = None, level=logging.INFO) -> logging.Logger:
    if log_path is None:
        log_dir = os.path.join(os.getcwd(), "logs")
        os.makedirs(log_dir, exist_ok=True)
        log_path = os.path.join(log_dir, f"automation_{datetime.now().strftime('%Y-%m-%d')}.log")

    logger = logging.getLogger(name)
    logger.setLevel(level)

    logger.propagate = False

    if not logger.handlers:
        format_str = "%(asctime)s [%(levelname)s] [%(name)s]: %(message)s"
        formatter = logging.Formatter(format_str, "%H:%M:%S")

        fh = logging.FileHandler(log_path, mode="a", encoding="utf-8")
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    return logger
