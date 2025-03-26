import logging

# Настройка базовой конфигурации логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)


def create_logger(name="api"):
    return logging.getLogger(name)
