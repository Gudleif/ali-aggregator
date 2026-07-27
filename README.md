# Top Ali Aggregator

Высокопроизводительный агрегатор товаров и автоматизированный конвейер данных для работы с партнерскими сетями (AliExpress), построенный на базе Django, Celery, Redis и Docker.

## Основной функционал
*   **Автоматизированный ETL-конвейер данных**: Фоновая выгрузка, парсинг и импорт товарных фидов по расписанию (Celery + Celery Beat). Включает фильтрацию спама, валидацию, дедупликацию и расчет внутреннего рейтинга товаров (`internal_score`).
*   **Динамическое управление каталогом и ранжирование**: Автоматическое управление видимостью товаров (`is_active`) при еженедельных обновлениях каталога — скрытие позиций со спам-словами или нулевым рейтингом и их автоматическая активация при улучшении показателей. Витрина и API отсортированы строго по убыванию рейтинга выгоды (`-internal_score`).
*   **Продвинутая SEO-архитектура и перелинковка**: Чистый серверный рендеринг (SSR), динамические Meta-теги, защита от дублей через Canonical URL и строгая иерархия. Внедрены автоматические «хлебные крошки» (Breadcrumbs), блоки смежных категорий («Related Categories») и глубокая перелинковка (Deep Linking) через футер для эффективного распределения ссылочного веса и удержания краулеров.
*   **Поисковая микроразметка (Schema.org JSON-LD)**: Вшитые структурированные данные для списков (`ItemList`) и цепочек навигации (`BreadcrumbList`), обеспечивающие отображение расширенных сниппетов (Rich Snippets) в поисковой выдаче Google.
*   **Система монетизации и аналитика кликов**: Умная маршрутизация партнерских ссылок с fallback-защитой и автоматическим логированием переходов (`ClickLog`), фиксирующим IP-адреса, User-Agent и ID товаров для контроля конверсии.
*   **Молниеносное кэширование API**: Оптимизация времени отклика REST API до 2–5 миллисекунд с помощью Redis и `django-redis`. Реализована автоматическая инвалидация (сброс) кэша сразу после завершения импорта новых данных.
*   **Гибкий REST API**: Полнофункциональный API (Django REST Framework) с фильтрацией категорий и брендов, полнотекстовым поиском, пагинацией и оптимизированными SQL-запросами (`select_related`).
*   **Комплексное тестирование (QA Suite)**: Полное покрытие критической бизнес-логики автоматизированными тестами на базе `pytest`. Протестированы кастомные management-команды, математика скоринга, изоляция скрытых товаров, SQL-оптимизация и безопасность партнерских редиректов.
*   **Безопасность и очистка ресурсов**: Автоматическое удаление временных CSV-файлов после обработки, разделение логических баз данных Redis для задач и кэша, хранение конфиденциальных токенов в `.env`.
*   **Изолированная Docker-инфраструктура**: Полный запуск проекта одной командой через Docker Compose, объединяющий 5 связанных сервисов (Web, Postgres, Redis, Celery Worker, Celery Beat).

## Технологический стек
*   **Backend**: Python 3.x, Django 5.x, Django REST Framework, Django Filter
*   **Тестирование и контроль качества**: Pytest, Pytest-Django
*   **Асинхронность и задачи**: Celery, Celery Beat
*   **Кэширование и очереди**: Redis, `django-redis` (с разделением Redis DB 0 для Celery и DB 1 для кэша API)
*   **База данных**: PostgreSQL
*   **Сетевые клиенты**: Requests
*   **DevOps & Инфраструктура**: Docker, Docker Compose

## Лицензия и авторские права
© 2026 Gudleif. Все права защищены.

Данный репозиторий предоставляется исключительно в демонстрационных целях (в качестве портфолио).
Любое копирование, модификация, распространение или коммерческое использование данного кода без прямого разрешения автора строго запрещено.

---

# Top Ali Aggregator

A high-performance product aggregator and automated data pipeline designed for affiliate marketing networks (AliExpress), built with Django, Celery, Redis, and Docker.

## Key Features
*   **Automated ETL Data Pipeline**: Scheduled background fetching, parsing, and processing of product CSV feeds via Celery & Celery Beat. Includes spam filtering, validation, deduplication, and custom product ranking (`internal_score`).
*   **Dynamic Catalog Management & Ranking**: Automated visibility control (`is_active`) during weekly feed updates—instant hiding of spam or zero-score items and automatic reactivation when metrics improve. Storefront and API responses are strictly ordered by profitability (`-internal_score`).
*   **Advanced SEO Architecture & Internal Linking**: Full Server-Side Rendering (SSR), dynamic meta tags, duplicate protection via canonical URLs, and strict hierarchy. Features automated breadcrumbs, cross-linked "Related Categories" blocks, and footer deep-linking to optimize crawler indexation and page rank distribution.
*   **Structured Data (Schema.org JSON-LD)**: Embedded structured data for product lists (`ItemList`) and navigation chains (`BreadcrumbList`), enabling rich snippets in Google search results.
*   **Monetization Engine & Click Analytics**: Smart affiliate link routing with fallback protection and automated click logging (`ClickLog`), capturing IP addresses, User-Agent strings, and product IDs for conversion tracking.
*   **Sub-Millisecond API Caching**: REST API response optimization down to 2–5 ms using Redis and `django-redis`. Features smart automatic cache invalidation triggered right after data import completion.
*   **Flexible REST API**: Fully-featured DRF API providing category/brand filtering, full-text search, custom pagination, and optimized ORM queries (`select_related`).
*   **Comprehensive QA & Test Suite**: End-to-end automated testing powered by `pytest`. Covers custom management commands, scoring algorithms, hidden product isolation, ORM query optimization, and redirect security.
*   **Resource Management & Security**: Guaranteed disk cleanup of temporary feed files post-import, separation of Redis logical databases for queues and cache, and safe `.env` configuration management.
*   **Full Containerization**: One-command architecture deployment with Docker Compose, orchestrating 5 isolated services (Web, Postgres, Redis, Celery Worker, Celery Beat).

## Tech Stack
*   **Backend**: Python 3.x, Django 5.x, Django REST Framework, Django Filter
*   **Testing & Quality Assurance**: Pytest, Pytest-Django
*   **Async & Task Scheduling**: Celery, Celery Beat
*   **In-Memory Store & Caching**: Redis, `django-redis` (Isolated Redis DB 0 for Celery, DB 1 for API Cache)
*   **Database**: PostgreSQL
*   **Networking**: Requests
*   **DevOps & Infrastructure**: Docker, Docker Compose

## License and Copyright
© 2026 Gudleif. All rights reserved.

This repository is provided solely for demonstration purposes (as a portfolio project). 
Any copying, modification, distribution, or commercial use of this code without the author's express permission is strictly prohibited.