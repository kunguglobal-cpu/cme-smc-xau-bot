import logging
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "bot.log"

logger = logging.getLogger("CME_SMC_XAU")
logger.setLevel(logging.INFO)

if not logger.handlers:
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


def log_signal(signal):
    logger.info(
        "SIGNAL | direction=%s | reason=%s",
        signal.get("direction"),
        signal.get("reason"),
    )


def log_event(message):
    logger.info(message)


def log_error(message):
    logger.error(message)
