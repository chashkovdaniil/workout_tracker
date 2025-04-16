import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

# Создаем директорию для логов, если она не существует
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

# Формат логов
log_format = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Обработчик для файла
file_handler = RotatingFileHandler(
    "logs/app.log",
    maxBytes=10_000_000,  # 10MB
    backupCount=5,
    encoding="utf-8"
)
file_handler.setFormatter(log_format)
file_handler.setLevel(logging.INFO)

# Обработчик для консоли
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(log_format)
console_handler.setLevel(logging.DEBUG)

# Настройка корневого логгера
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)
root_logger.addHandler(file_handler)
root_logger.addHandler(console_handler)

# Настройка логгера для SQL запросов
sql_logger = logging.getLogger("sqlalchemy.engine")
sql_logger.setLevel(logging.WARNING)

# Настройка логгера для FastAPI
fastapi_logger = logging.getLogger("uvicorn")
fastapi_logger.setLevel(logging.INFO)

def get_logger(name: str) -> logging.Logger:
    """Получение логгера с указанным именем."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    return logger 