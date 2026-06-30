import logging
import config
from pathlib import Path

# Create logger
logger = logging.getLogger(config.PROJECT_NAME)
logger.setLevel(getattr(logging, config.LOG_LEVEL))

# Create formatters
formatter = logging.Formatter(
    '[%(asctime)s] [%(levelname)s] %(name)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# File handler
log_file = Path(config.LOG_FILE)
log_file.parent.mkdir(parents=True, exist_ok=True)
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(getattr(logging, config.LOG_LEVEL))
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(getattr(logging, config.LOG_LEVEL))
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Prevent duplicate logs
logger.propagate = False
