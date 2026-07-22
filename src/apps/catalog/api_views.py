from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from apps.catalog.models import Product, Category, Brand
from apps.catalog.serializers import ProductSerializer, CategorySerializer, BrandSerializer
from apps.catalog.filters import ProductFilter


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_class = ProductFilter

    search_fields = ['name', 'brand__name']

    def get_queryset(self):
        return Product.objects.select_related('category', 'brand') \
            .filter(is_active=True) \
            .order_by('-internal_score')

    # Оборачиваем метод списка в кэш на 1 час (60 секунд * 60 минут)
    @method_decorator(cache_page(60 * 60))
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        filtered_queryset = self.filter_queryset(queryset)
        sliced_queryset = filtered_queryset[:50]

        serializer = self.get_serializer(sliced_queryset, many=True)
        return Response(serializer.data)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    # Кэшируем список категорий на 1 час
    @method_decorator(cache_page(60 * 60))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class BrandViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

    # Кэшируем список брендов на 1 час
    @method_decorator(cache_page(60 * 60))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)