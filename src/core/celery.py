import os
from celery import Celery

# Устанавливаем настройки Django по умолчанию для Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Создаем экземпляр приложения Celery
app = Celery('core')

# Загружаем настройки из файла settings.py
# namespace='CELERY' означает, что все настройки Celery там должны начинаться с префикса CELERY_
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически находим задачи (файлы tasks.py) во всех установленных приложениях Django
app.autodiscover_tasks()