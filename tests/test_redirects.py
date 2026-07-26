import pytest
from django.urls import reverse
from apps.catalog.models import Product, Category, Brand, ClickLog

# Помечаем, что этому файлу разрешено работать с базой данных
pytestmark = pytest.mark.django_db


@pytest.fixture
def sample_product():
    """
    Создаем тестовый товар с партнерской ссылкой.
    Эта фикстура будет передаваться в аргументы теста.
    """
    category = Category.objects.create(name="Видеокарты", slug="videocards")
    brand = Brand.objects.create(name="NVIDIA", slug="nvidia")

    product = Product.objects.create(
        name="RTX 4060 Ti",
        slug="rtx-4060-ti",
        price=399.99,
        category=category,
        brand=brand,
        affiliate_url="https://ali.ski/test_affiliate_link",
        is_active=True
    )
    return product


def test_product_redirect_and_analytics(client, sample_product):
    """
    Проверяем, что при переходе по нашей внутренней ссылке происходит
    редирект на сайт партнера и создается запись в логах аналитики.
    """
    # 1. Проверяем, что до клика таблица аналитики пуста
    assert ClickLog.objects.count() == 0, "Перед тестом лог кликов должен быть пустым"

    # 2. Формируем URL автоматически по имени маршрута и параметру 'product_id'
    redirect_url = reverse('product_buy', kwargs={'product_id': sample_product.id})

    # 3. Эмулируем переход пользователя с помощью встроенного веб-клиента
    response = client.get(
        redirect_url,
        HTTP_USER_AGENT="Mozilla/5.0 Test Browser",
        REMOTE_ADDR="192.168.1.50"
    )

    # 4. ПРОВЕРКА 1: Сервер должен ответить кодом 302 (Временный редирект)
    assert response.status_code == 302, f"Ожидался статус 302, получен {response.status_code}"

    # 5. ПРОВЕРКА 2: Пользователя должно перебросить ровно на нашу партнерскую ссылку
    assert response.url == "https://ali.ski/test_affiliate_link"

    # 6. ПРОВЕРКА 3: В базе данных должна появиться ровно 1 запись о клике
    assert ClickLog.objects.count() == 1, "Клик не записался в базу данных ClickLog"

    # 7. ПРОВЕРКА 4: Проверяем качество сохраненных данных аналитики
    log_entry = ClickLog.objects.first()
    assert log_entry.product == sample_product
    assert log_entry.ip_address == "192.168.1.50"
    assert "Test Browser" in log_entry.user_agent