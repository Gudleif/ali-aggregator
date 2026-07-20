import django_filters
from apps.catalog.models import Product


class ProductFilter(django_filters.FilterSet):
    # Позволяем искать диапазоны цен: ?min_price=10&max_price=50
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr='lte')

    # Фильтруем по слагу категории, а не по ID (чтобы URL были красивыми)
    category = django_filters.CharFilter(field_name='category__slug')
    brand = django_filters.CharFilter(field_name='brand__slug')

    class Meta:
        model = Product
        fields = ['category', 'brand', 'min_price', 'max_price']