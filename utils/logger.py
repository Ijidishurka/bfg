import logging
import os

log_level = logging.ERROR
log_file_path = "bot_errors.txt"
max_log_size = 1024 * 100


def check_log_size() -> None:
    if os.path.exists(log_file_path) and os.path.getsize(log_file_path) > max_log_size:
        with open(log_file_path, "w") as log_file:
            log_file.truncate(0)


check_log_size()

logger = logging.getLogger()
logger.setLevel(log_level)


formatter = logging.Formatter(
    fmt="%(asctime)s - %(levelname)s %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)


file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
file_handler.setLevel(log_level)
file_handler.setFormatter(formatter)


console_handler = logging.StreamHandler()
console_handler.setLevel(log_level)
console_handler.setFormatter(formatter)


logger.addHandler(file_handler)
logger.addHandler(console_handler)
