import os
import logging
import requests
from celery import shared_task
from django.core.management import call_command
from django.conf import settings

logger = logging.getLogger(__name__)


@shared_task
def process_price_range_csv(file_url: str, range_label: str = "default"):
    """
    Скачивает CSV по прямой ссылке, импортирует в БД и сразу удаляет файл.
    """
    logger.info(f"Запуск импорта для диапазона '{range_label}' по ссылке: {file_url}")

    # Путь к временному файлу на диске
    temp_file_path = os.path.join(settings.BASE_DIR, f"temp_{range_label}.csv")

    try:
        # 1. Скачивание файла частями (stream=True), чтобы не забивать RAM
        response = requests.get(file_url, stream=True, timeout=120)
        response.raise_for_status()

        with open(temp_file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        logger.info(f"Файл {range_label} успешно скачан: {temp_file_path}")

        # 2. Вызов команды импорта в БД
        # Передаем путь к файлу в команду (если твоя команда import_products принимает аргументы)
        logger.info(f"Начало записи данных из {range_label} в БД...")
        call_command('import_products', temp_file_path)
        logger.info(f"Импорт файла {range_label} завершен!")

        return f"Успешно обработан {range_label}"

    except Exception as e:
        logger.error(f"Ошибка при обработке диапазона {range_label}: {e}")
        return f"Ошибка: {e}"

    finally:
        # 3. Гарантированное удаление файла с диска
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
            logger.info(f"Временный файл удален с диска: {temp_file_path}")