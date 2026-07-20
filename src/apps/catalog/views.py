from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView
from .models import Product, ClickLog


class ProductRedirectView(View):
    def get(self, request, product_id, *args, **kwargs):
        # 1. Ищем товар
        product = get_object_or_404(Product, id=product_id, is_active=True)

        # 2. Определяем IP-адрес
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0]
        else:
            ip_address = request.META.get('REMOTE_ADDR')

        # 3. Получаем User-Agent
        user_agent = request.META.get('HTTP_USER_AGENT', '')

        # 4. Сохраняем лог клика
        ClickLog.objects.create(
            product=product,
            ip_address=ip_address,
            user_agent=user_agent
        )

        # 5. Гибкая логика маршрутизации (Приоритет: affiliate -> original -> fallback)
        if product.affiliate_url:
            target_url = product.affiliate_url
        elif product.original_url:
            target_url = product.original_url
        else:
            # Предохранитель: если обе ссылки пустые, возвращаем юзера на витрину
            return redirect('/')

        # === ДЕБАГ В ТЕРМИНАЛ ===
        # Этот блок выведет информацию прямо в твою консоль Docker
        print("\n" + "="*50)
        print("=== ДЕБАГ ПАРТНЕРСКОГО РЕДИРЕКТА ===")
        print(f"1. Товар: {product.name} (ID: {product.id})")
        print(f"2. Наличие Affiliate URL: {bool(product.affiliate_url)}")
        print(f"3. Наличие Original URL: {bool(product.original_url)}")
        print(f"4. ИТОГОВЫЙ ПЕРЕХОД: {target_url}")
        print("="*50 + "\n")
        # =======================

        return redirect(target_url)


# Класс для витрины
class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'

    # Вытаскиваем только активные товары и оптимизируем SQL-запрос
    def get_queryset(self):
        return Product.objects.filter(is_active=True).select_related('category', 'brand')