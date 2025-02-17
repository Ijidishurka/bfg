import logging
import install
import os


log_file_path = 'commands/admin/bot_errors.txt'
max_log_size = 1024 * 100


def check_log_size() -> None:
    if os.path.exists(log_file_path) and os.path.getsize(log_file_path) > max_log_size:
        with open(log_file_path, 'w') as log_file:
            log_file.truncate(0)


logging.basicConfig(
    filename=log_file_path,
    level=logging.WARNING,
    format='%(asctime)s - %(levelname)s %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

check_log_size()