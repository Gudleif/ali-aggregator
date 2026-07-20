# src/apps/catalog/api_urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import ProductViewSet, CategoryViewSet, BrandViewSet

# Обязательно указываем app_name для изоляции (namespace)
app_name = 'catalog_api'

# Настраиваем роутер
router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'categories', CategoryViewSet)
router.register(r'brands', BrandViewSet)

urlpatterns = [
    # Все пути роутера будут доступны по этому адресу
    path('', include(router.urls)),
]