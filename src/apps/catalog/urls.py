from django.contrib import admin
from django.urls import path
from django.contrib.sitemaps.views import sitemap
from django.http import HttpResponse
from apps.catalog.views import ProductRedirectView, ProductListView
from apps.catalog.sitemaps import StorefrontSitemap

# Регистрируем только реальную карту витрины
sitemaps = {
    'storefront': StorefrontSitemap,
}


# Динамический генератор правила robots.txt
def robots_txt(request):
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        "Disallow: /redirect/",  # Строго запрещаем роботам кликать по партнерским редиректам
        "Disallow: /*?*",        # Запрещаем индексировать мусор с GET-параметрами (сортировки, UTM)
        "Allow: /$",             # Разрешаем индексировать только главную витрину
        f"Sitemap: {request.build_absolute_uri('/sitemap.xml')}",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


urlpatterns = [
    path('admin/', admin.site.urls),

    # 1. SEO-МАРШРУТЫ
    path('robots.txt', robots_txt, name='robots_txt'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    # 2. ВИТРИНА И РЕДИРЕКТЫ
    path('', ProductListView.as_view(), name='product_list'),
    path('redirect/<int:product_id>/', ProductRedirectView.as_view(), name='product_buy'),
]