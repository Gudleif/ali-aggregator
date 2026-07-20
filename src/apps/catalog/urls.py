# src/apps/catalog/urls.py
from django.urls import path
from .views import ProductRedirectView, ProductListView

# Убираем или комментируем app_name, чтобы вернуть глобальную видимость для шаблонов
# app_name = 'catalog'

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),

    # Меняем name на 'product_buy', чтобы фронтенд сразу нашёл эту ссылку!
    path('redirect/<int:product_id>/', ProductRedirectView.as_view(), name='product_buy'),
]