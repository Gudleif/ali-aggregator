from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.filters import SearchFilter  # ИМПОРТИРУЕМ СТАНДАРТНЫЙ ПОИСК
from django_filters.rest_framework import DjangoFilterBackend
from apps.catalog.models import Product, Category, Brand
from apps.catalog.serializers import ProductSerializer, CategorySerializer, BrandSerializer
from apps.catalog.filters import ProductFilter


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProductSerializer
    # Добавляем SearchFilter в список бэкендов фильтрации
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_class = ProductFilter

    # Указываем, по каким полям искать (по названию товара и по имени бренда)
    search_fields = ['name', 'brand__name']

    def get_queryset(self):
        return Product.objects.select_related('category', 'brand') \
            .filter(is_active=True) \
            .order_by('-internal_score')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        filtered_queryset = self.filter_queryset(queryset)
        sliced_queryset = filtered_queryset[:50]

        serializer = self.get_serializer(sliced_queryset, many=True)
        return Response(serializer.data)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class BrandViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer