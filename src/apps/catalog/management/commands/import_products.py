import csv
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from apps.catalog.models import Product, Category, Brand


class Command(BaseCommand):
    help = 'Импорт боевых данных из Admitad CSV с расчетом рейтинга качества'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Путь к CSV файлу (например, src/goods_combat.csv)')

    def _parse_param_field(self, param_string):
        """Безопасно извлекает commissionRate и shopId из строки вида discount|41%|;commissionRate|7.69%|"""
        data = {'commission_rate': 0.0, 'shop_id': None}
        if not param_string:
            return data

        parts = param_string.replace('"', '').split(';')
        for part in parts:
            if 'commissionRate|' in part:
                try:
                    val = part.split('|')[1].replace('%', '')
                    data['commission_rate'] = float(val)
                except (IndexError, ValueError):
                    pass
            elif 'shopId|' in part:
                try:
                    data['shop_id'] = part.split('|')[1].strip()
                except IndexError:
                    pass
        return data

    def handle(self, *args, **options):
        file_path = options['csv_file']
        self.stdout.write(f"Начинаем импорт из: {file_path}...")

        created_count = 0
        updated_count = 0

        # Словарь для отслеживания спама: сколько товаров от конкретного магазина мы встретили
        shop_density_tracker = {}

        # Список стоп-слов для жесткого бана мусора/аксессуаров
        stop_words = [
            'box only', 'empty box', 'case for', 'чехол для',
            'кабель для', 'коробка от', 'реплика', 'только коробка'
        ]

        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=';')

            for row in reader:
                try:
                    # 1. Читаем базовые данные
                    # Обрезаем название до 500 символов, чтобы избежать ошибки БД "value too long"
                    name = row['name'].strip()[:500]
                    category_name = row['category'].strip()
                    price = float(row['price'])
                    old_price = float(row['oldprice']) if row.get('oldprice') else price
                    affiliate_url = row['url'].strip()
                    image_url = row['picture'].strip()
                    ali_id = str(row['id']).strip()

                    # 2. Вытаскиваем параметры из param
                    param_string = row.get('param', '')
                    extracted_params = self._parse_param_field(param_string)
                    commission_rate = extracted_params['commission_rate']
                    shop_id = extracted_params['shop_id']

                    # 3. Расчет умного рейтинга качества (internal_score)
                    discount_score = 0.0
                    if old_price > price and old_price > 0:
                        discount_pct = ((old_price - price) / old_price) * 100
                        if 5.0 <= discount_pct <= 60.0:
                            discount_score = discount_pct * 0.5

                    internal_score = commission_rate + discount_score

                    # Антиспам 1: Стоп-слова
                    if any(word in name.lower() for word in stop_words):
                        internal_score = 0.0

                    # Антиспам 2: Лимит на один магазин
                    if shop_id:
                        shop_density_tracker[shop_id] = shop_density_tracker.get(shop_id, 0) + 1
                        if shop_density_tracker[shop_id] > 5:
                            internal_score = 0.0

                    # 4. Определение категории
                    cat_slug = slugify(category_name)
                    if not cat_slug:
                        cat_slug = f"category-{abs(hash(category_name))}"

                    category, _ = Category.objects.get_or_create(
                        slug=cat_slug,
                        defaults={'name': category_name}
                    )

                    # --- УМНАЯ ПРОВЕРКА БРЕНДА ---
                    brand = None
                    raw_brand_name = row.get('brand')

                    # Создаем бренд только если колонка существует и не пустая
                    if raw_brand_name and raw_brand_name.strip():
                        clean_brand_name = raw_brand_name.strip()[:50]
                        brand_slug = slugify(clean_brand_name)

                        if not brand_slug:
                            brand_slug = f"brand-{abs(hash(clean_brand_name))}"

                        brand, _ = Brand.objects.get_or_create(
                            slug=brand_slug,
                            defaults={'name': clean_brand_name}
                        )

                    # Уникальный слаг на основе ID AliExpress (не зависит от бренда)
                    product_slug = f"item-{ali_id}"

                    # 5. Ищем по УНИКАЛЬНОМУ СЛАГУ, чтобы не плодить дубликаты и не вызывать ошибок бд
                    product, created = Product.objects.update_or_create(
                        slug=product_slug,
                        defaults={
                            'ali_id': ali_id,
                            'name': name,
                            'category': category,
                            'brand': brand,
                            'price': price,
                            'old_price': old_price,
                            'shop_id': shop_id,
                            'commission_rate': commission_rate,
                            'internal_score': internal_score,
                            'original_url': affiliate_url,
                            'image_url': image_url,
                        }
                    )

                    if created:
                        created_count += 1
                    else:
                        updated_count += 1

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Ошибка в строке {row.get('id', 'Unknown')}: {e}"))
                    continue

        self.stdout.write(
            self.style.SUCCESS(
                f"Импорт успешно завершен! Создано товаров: {created_count}, Обновлено: {updated_count}"))
