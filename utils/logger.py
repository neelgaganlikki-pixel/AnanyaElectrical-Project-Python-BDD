import logging
import os
import sys

def get_logger(name: str = "AnanyaAutomation") -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        
        # Console Handler
        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

        # File Handler
        log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports", "logs")
        os.makedirs(log_dir, exist_ok=True)
        fh = logging.FileHandler(os.path.join(log_dir, "automation.log"), encoding="utf-8")
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger

