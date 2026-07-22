# PC Ali Aggregator

Высокопроизводительный агрегатор товаров и автоматизированный конвейер данных для работы с партнерскими сетями (AliExpress), построенный на базе Django, Celery, Redis и Docker.

## Основной функционал
*   **Автоматизированный ETL-конвейер данных**: Фоновая выгрузка, парсинг и импорт товарных фидов по расписанию (Celery + Celery Beat). Включает фильтрацию спама, валидацию, дедупликацию и расчет внутреннего рейтинга товаров (`internal_score`).
*   **Молниеносное кэширование API**: Оптимизация времени отклика REST API до 2–5 миллисекунд с помощью Redis и `django-redis`. Реализована автоматическая инвалидация (сброс) кэша сразу после завершения импорта новых данных.
*   **Гибкий REST API**: Полнофункциональный API (Django REST Framework) с фильтрацией категорий и брендов, полнотекстовым поиском, пагинацией и оптимизированными SQL-запросами (`select_related`).
*   **Безопасность и очистка ресурсов**: Автоматическое удаление временных CSV-файлов после обработки, разделение логических баз данных Redis для задач и кэша, хранение конфиденциальных токенов в `.env`.
*   **Изолированная Docker-инфраструктура**: Полный запуск проекта одной командой через Docker Compose, объединяющий 6 связанных сервисов (Web, Postgres, Redis, Celery Worker, Celery Beat, Selenium).

## Технологический стек
*   **Backend**: Python 3.x, Django 5.x, Django REST Framework, Django Filter
*   **Асинхронность и задачи**: Celery, Celery Beat
*   **Кэширование и очереди**: Redis, `django-redis` (с разделением Redis DB 0 для Celery и DB 1 для кэша API)
*   **База данных**: PostgreSQL
*   **Автоматизация и сетевые клиенты**: Requests, Selenium (Headless Chrome)
*   **DevOps & Инфраструктура**: Docker, Docker Compose

## Лицензия и авторские права
© 2026 Gudleif. Все права защищены.

Данный репозиторий предоставляется исключительно в демонстрационных целях (в качестве портфолио).
Любое копирование, модификация, распространение или коммерческое использование данного кода без прямого разрешения автора строго запрещено.

---

# PC Ali Aggregator

A high-performance product aggregator and automated data pipeline designed for affiliate marketing networks (AliExpress), built with Django, Celery, Redis, and Docker.

## Key Features
*   **Automated ETL Data Pipeline**: Scheduled background fetching, parsing, and processing of product CSV feeds via Celery & Celery Beat. Includes spam filtering, validation, deduplication, and custom product ranking (`internal_score`).
*   **Sub-Millisecond API Caching**: REST API response optimization down to 2–5 ms using Redis and `django-redis`. Features smart automatic cache invalidation triggered right after data import completion.
*   **Flexible REST API**: Fully-featured DRF API providing category/brand filtering, full-text search, custom pagination, and optimized ORM queries (`select_related`).
*   **Resource Management & Security**: Guaranteed disk cleanup of temporary feed files post-import, separation of Redis logical databases for queues and cache, and safe `.env` configuration management.
*   **Full Containerization**: One-command architecture deployment with Docker Compose, orchestrating 6 isolated services (Web, Postgres, Redis, Celery Worker, Celery Beat, Selenium).

## Tech Stack
*   **Backend**: Python 3.x, Django 5.x, Django REST Framework, Django Filter
*   **Async & Task Scheduling**: Celery, Celery Beat
*   **In-Memory Store & Caching**: Redis, `django-redis` (Isolated Redis DB 0 for Celery, DB 1 for API Cache)
*   **Database**: PostgreSQL
*   **Automation & Networking**: Requests, Selenium (Headless Chrome)
*   **DevOps & Infrastructure**: Docker, Docker Compose

## License and Copyright
© 2026 Gudleif. All rights reserved.

This repository is provided solely for demonstration purposes (as a portfolio project). 
Any copying, modification, distribution, or commercial use of this code without the author's express permission is strictly prohibited.
