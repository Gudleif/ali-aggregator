from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StorefrontSitemap(Sitemap):
    priority = 1.0          # Максимальный приоритет для главной страницы
    changefreq = 'daily'    # Подсказываем Google, что ассортимент и скидки меняются каждый день

    def items(self):
        return ['product_list']  # Название нашего главного маршрута из urls.py

    def location(self, item):
        return reverse(item)     # Django автоматически превратит 'product_list' в корень '/'