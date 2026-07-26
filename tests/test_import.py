import pytest
from django.core.management import call_command
from apps.catalog.models import Product, Category, Brand

# Разрешаем тесту работать с базой данных
pytestmark = pytest.mark.django_db


def test_import_command_and_scoring(tmp_path):
    """
    Тестируем реальную команду импорта:
    1. Корректный расчет internal_score (комиссия + бонус за скидку).
    2. Срабатывание антиспама по стоп-словам (score сбрасывается в 0.0).
    3. Защита от дубликатов (update_or_create по уникальному slug).
    """
    # 1. Создаем во временной папке мини-версию CSV файла для теста
    csv_file = tmp_path / "test_goods.csv"

    # Записываем тестовые строки в формате Admitad CSV (разделитель — точка с запятой)
    # Первая строка — нормальный товар, вторая — мусор со стоп-словом "empty box"
    csv_content = (
        "id;name;category;price;oldprice;url;picture;param;brand\n"
        "501;Ryzen 5 7500F;Computer Components;140.00;180.00;https://ali.ski/1;https://img.com/1;commissionRate|7.5%|;shopId|100;AMD\n"
        "502;Empty Box for GPU;Computer Components;10.00;;https://ali.ski/2;https://img.com/2;commissionRate|5.0%|;shopId|100;NVIDIA\n"
    )
    csv_file.write_text(csv_content, encoding="utf-8")

    # 2. Запускаем нашу Django management-команду импорта (передаем путь к фейковому CSV)
    # Замени 'import_combat_data' на точное имя файла твоей команды в management/commands/ (без .py)
    call_command('import_products', str(csv_file))

    # 3. ПРОВЕРКА 1: Товары успешно импортировались (в базе ровно 2 товара)
    assert Product.objects.count() == 2

    # 4. ПРОВЕРКА 2: Обычный товар получил честно рассчитанный internal_score > 0
    good_product = Product.objects.get(ali_id="501")
    assert good_product.name == "Ryzen 5 7500F"
    assert good_product.commission_rate == 7.5
    assert good_product.internal_score > 0, "У нормального товара должен быть рассчитан скор"

    # 5. ПРОВЕРКА 3: Товар со стоп-словом ("Empty Box") распознан антиспамом и его скор обнулен
    bad_product = Product.objects.get(ali_id="502")
    assert bad_product.internal_score == 0.0, "Антиспам должен сбросить internal_score до 0.0 для мусора"

    # 6. ПРОВЕРКА 4: Защита от дубликатов. Повторный запуск импорта того же файла не должен плодить строки
    call_command('import_products', str(csv_file))
    assert Product.objects.count() == 2, "Повторный импорт не должен создавать новые дубликаты в БД"