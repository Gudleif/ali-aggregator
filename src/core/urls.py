# src/config/urls.py (или твой главный urls.py проекта)
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # 1. ОБЫЧНЫЕ СТРАНИЦЫ (Убрали namespace, чтобы не ломать старый фронтенд)
    path('', include('apps.catalog.urls')),

    # 2. НАШЕ API (Оставляем изолированным и версионированным)
    path('api/v1/catalog/', include('apps.catalog.api_urls', namespace='catalog_api')),
]