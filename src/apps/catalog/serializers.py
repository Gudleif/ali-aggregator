from rest_framework import serializers
from .models import Product, Category, Brand


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'slug']


class ProductSerializer(serializers.ModelSerializer):
    # Вкладываем сериализаторы, чтобы вместо просто ID категории/бренда
    # в JSON отдавались их названия и данные
    category = CategorySerializer(read_only=True)
    brand = BrandSerializer(read_only=True)

    # ВАЖНАЯ БИЗНЕС-ЛОГИКА:
    # Мы генерируем ссылку на наш внутренний редирект,
    # а не отдаем наружу чистую реф-ссылку (affiliate_url).
    # Так никто не сможет обойти нашу систему учета кликов!
    redirect_url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'slug',
            'price',
            'image_url',
            'category',
            'brand',
            'redirect_url'
        ]

    def get_redirect_url(self, obj):
        # Генерируем путь к твоей вьюхе ProductRedirectView.
        # Обрати внимание: если у тебя в urls.py редирект настроен по id, оставляем obj.id
        return f"/redirect/{obj.id}/"