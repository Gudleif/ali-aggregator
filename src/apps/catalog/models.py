from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Category Name")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="URL Slug")
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subcategories',
        verbose_name="Parent Category"
    )

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' -> '.join(full_path[::-1])


class Brand(models.Model):
    name = models.CharField(max_length=255, verbose_name="Brand Name")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="URL Slug")
    description = models.TextField(blank=True, verbose_name="Description")

    class Meta:
        verbose_name = "Brand"
        verbose_name_plural = "Brands"
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name="Category"
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products',
        verbose_name="Brand"
    )
    name = models.CharField(max_length=500, verbose_name="Product Name")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="URL Slug")
    description = models.TextField(blank=True, verbose_name="Description")

    # Цены
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (USD)")
    old_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                    verbose_name="Old Price (USD)")

    # Уникальные идентификаторы AliExpress
    ali_id = models.CharField(max_length=50, unique=True, null=True, blank=True, verbose_name="AliExpress ID")
    shop_id = models.CharField(max_length=50, blank=True, null=True, verbose_name="Shop ID")

    # Коммерческие метрики
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.0,
                                          verbose_name="Commission Rate (%)")

    # НАШ ВНУТРЕННИЙ РЕЙТИНГ КАЧЕСТВА (Индексирован для сверхбыстрой сортировки в API)
    internal_score = models.DecimalField(max_digits=8, decimal_places=2, default=0.0, db_index=True,
                                         verbose_name="Internal Quality Score")

    # Ссылки (оригинальная и партнерская Admitad)
    original_url = models.URLField(max_length=1000, verbose_name="Original AliExpress URL")
    affiliate_url = models.URLField(max_length=1000, blank=True, verbose_name="Admitad Affiliate URL")

    # Прямая ссылка на картинку товара
    image_url = models.URLField(null=True, blank=True, max_length=1000, verbose_name="Product Image URL")

    is_active = models.BooleanField(default=True, verbose_name="Is Active")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ['-internal_score', '-created_at']

    def __str__(self):
        return self.name

    @property
    def display_score(self):
        """
        Преобразует внутренний скор (партнерскую выгоду) в красивый 5-балльный рейтинг для покупателей.
        """
        score = self.internal_score or 0
        if score >= 30:
            return "5.0"
        elif score >= 20:
            return "4.9"
        elif score >= 5:
            return "4.8"
        else:
            return "4.7"

    @property
    def redirect_url(self):
        return f"/redirect/{self.id}/"


class ClickLog(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='clicks',
        verbose_name="Product"
    )
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Clicked At")
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name="IP Address")
    user_agent = models.TextField(null=True, blank=True, verbose_name="User Agent")

    class Meta:
        verbose_name = "Click Log"
        verbose_name_plural = "Click Logs"
        ordering = ['-timestamp']

    def __str__(self):
        return f"Click on {self.product.name} at {self.timestamp}"
