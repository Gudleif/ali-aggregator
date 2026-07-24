import django_filters
from django.db.models import Q
from apps.catalog.models import Product


class ProductFilter(django_filters.FilterSet):
    # Позволяем искать диапазоны цен: ?min_price=10&max_price=50
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr='lte')

    # Фильтруем по слагу категории через кастомный метод (захватываем и дочерние разделы)
    category = django_filters.CharFilter(method='filter_by_category')
    brand = django_filters.CharFilter(field_name='brand__slug')

    class Meta:
        model = Product
        fields = ['category', 'brand', 'min_price', 'max_price']

    def filter_by_category(self, queryset, name, value):
        """
        Ищет товары, у которых slug совпадает либо с самой категорией (конечной),
        либо с родительской категорией (главным разделом).
        """
        return queryset.filter(
            Q(category__slug=value) | Q(category__parent__slug=value)
        )