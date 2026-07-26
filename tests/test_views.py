import pytest
from django.urls import reverse
from apps.catalog.models import Product, Category, Brand


@pytest.mark.django_db
class TestProductListView:
    @pytest.fixture(autouse=True)
    def setup_catalog_data(self):
        """Создаем тестовое окружение: категории, бренды и товары с разным скором."""
        self.category = Category.objects.create(name="Электроника", slug="electronics")
        self.brand = Brand.objects.create(name="Xiaomi", slug="xiaomi")

        # 1. Отличный товар с высоким рейтингом
        self.top_product = Product.objects.create(
            name="Xiaomi 13 Pro",
            slug="xiaomi-13-pro",
            ali_id="1001",
            category=self.category,
            brand=self.brand,
            price=50000,
            internal_score=25.0,
            is_active=True
        )

        # 2. Обычный товар с низким рейтингом
        self.low_score_product = Product.objects.create(
            name="Xiaomi Redmi 9",
            slug="xiaomi-redmi-9",
            ali_id="1002",
            category=self.category,
            brand=self.brand,
            price=10000,
            internal_score=5.0,
            is_active=True
        )

        # 3. Мусорный товар (со стоп-словом), который был отключен импортером
        self.hidden_trash_product = Product.objects.create(
            name="Empty Box for Xiaomi",
            slug="empty-box-xiaomi",
            ali_id="1003",
            category=self.category,
            brand=self.brand,
            price=100,
            internal_score=0.0,
            is_active=False  # <-- Скрыт от пользователей
        )

    def test_catalog_view_status_code_and_template(self, client):
        """Проверяем, что страница витрины открывается без ошибок (HTTP 200)."""
        # Если в твой urls.py путь витрины привязан к имени 'catalog-list' или 'home':
        # url = reverse('catalog:list')
        # Если витрина висит просто на главной странице '/', используем прямой путь:
        response = client.get('/')

        assert response.status_code == 200

    def test_catalog_view_filtering_and_sorting(self, client):
        """
        Главный тест витрины. Проверяет бизнес-логику:
        1. В контекст попадают ТОЛЬКО активные товары (is_active=True).
        2. Товары отсортированы строго по убыванию рейтинга (-internal_score).
        """
        response = client.get('/')

        # Получаем список товаров, который Django передал в HTML-шаблон
        products = list(response.context['products'])

        # Проверка 1: Изоляция мусора (в выдаче должно быть 2 товара из 3 созданных)
        assert len(products) == 2
        assert self.hidden_trash_product not in products

        # Проверка 2: Сортировка по скору (от большего к меньшему)
        assert products[0] == self.top_product
        assert products[1] == self.low_score_product
        assert products[0].internal_score > products[1].internal_score