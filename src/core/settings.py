import environ
from pathlib import Path
import os
from celery.schedules import crontab

# BASE_DIR указывает на папку src/
BASE_DIR = Path(__file__).resolve().parent.parent

# Инициализация environ
env = environ.Env(
    DEBUG=(bool, False) # Если DEBUG нет в .env, он будет False
)

# Читаем .env файл.
# Так как .env лежит в корне, мы берем родительскую папку от BASE_DIR:
env_file_path = BASE_DIR.parent / '.env'
environ.Env.read_env(env_file_path)

# Заменяем жестко прописанные секреты на переменные окружения
SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')

# Твоя база данных
DATABASES = {
    'default': env.db('DATABASE_URL', default=f'sqlite:///{BASE_DIR / "db.sqlite3"}')
}

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['*'])


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_filters',
    'apps.catalog',
    'django.contrib.sitemaps',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Настройки Admitad
ADMITAD_BASE_URL = env('ADMITAD_BASE_URL')

# --- CELERY SETTINGS ---
# Подтягиваем URL из переменных окружения (из файла .env)
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://redis:6379/0")

# Настройки сериализации (стандарт для безопасности и скорости)
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# Устанавливаем часовой пояс для планировщика такой же, как в Django
CELERY_TIMEZONE = TIME_ZONE

CSRF_TRUSTED_ORIGINS = [
    'https://top-ali.store',
    'https://www.top-ali.store',
]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Расписание запуска задач (Celery Beat)
CELERY_BEAT_SCHEDULE = {
    'import_range_1': {
        'task': 'apps.catalog.tasks.process_price_range_csv',
        'schedule': crontab(hour=2, minute=0, day_of_week=1),
        'args': (os.environ.get('ADMITAD_CSV_RANGE_1'), 'range_1'),
    },
    'import_range_2': {
        'task': 'apps.catalog.tasks.process_price_range_csv',
        'schedule': crontab(hour=2, minute=0, day_of_week=2),
        'args': (os.environ.get('ADMITAD_CSV_RANGE_2'), 'range_2'),
    },
    'import_range_3': {
        'task': 'apps.catalog.tasks.process_price_range_csv',
        'schedule': crontab(hour=2, minute=0, day_of_week=3),
        'args': (os.environ.get('ADMITAD_CSV_RANGE_3'), 'range_3'),
    },
    'import_range_4': {
        'task': 'apps.catalog.tasks.process_price_range_csv',
        'schedule': crontab(hour=2, minute=0, day_of_week=4),
        'args': (os.environ.get('ADMITAD_CSV_RANGE_4'), 'range_4'),
    },
    'import_range_5': {
        'task': 'apps.catalog.tasks.process_price_range_csv',
        'schedule': crontab(hour=2, minute=0, day_of_week=5),
        'args': (os.environ.get('ADMITAD_CSV_RANGE_5'), 'range_5'),
    },
    'import_range_6': {
        'task': 'apps.catalog.tasks.process_price_range_csv',
        'schedule': crontab(hour=2, minute=0, day_of_week=6),
        'args': (os.environ.get('ADMITAD_CSV_RANGE_6'), 'range_6'),
    },
    'import_range_7': {
        'task': 'apps.catalog.tasks.process_price_range_csv',
        'schedule': crontab(hour=1, minute=0, day_of_week=0),
        'args': (os.environ.get('ADMITAD_CSV_RANGE_7'), 'range_7'),
    },
    'import_range_8': {
        'task': 'apps.catalog.tasks.process_price_range_csv',
        'schedule': crontab(hour=5, minute=0, day_of_week=0),
        'args': (os.environ.get('ADMITAD_CSV_RANGE_8'), 'range_8'),
    },
}

# Настройки кэширования через Redis
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        # Убедись, что имя хоста совпадает с именем сервиса в docker-compose (например, redis или pc_redis)
        # Цифра /1 в конце означает базу данных №1
        "LOCATION": "redis://redis:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            # Игнорировать ошибки кэша (если Redis вдруг упадет, сайт продолжит работать через обычную БД)
            "IGNORE_EXCEPTIONS": True,
        }
    }
}

# Время жизни кэша по умолчанию (в секундах)
CACHE_TTL = 60 * 60  # 1 час