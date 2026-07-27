from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView
from .models import Product, Category, ClickLog


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
            return redirect('/')

        return redirect(target_url)


# Класс для гибридной витрины с серверной пагинацией и фильтрацией
class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'
    paginate_by = 30  # Количество товаров на одной странице

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True).select_related('category', 'brand').order_by(
            '-internal_score')

        category_slug = self.request.GET.get('category')
        if category_slug:
            # Ищем саму категорию
            category = Category.objects.filter(slug=category_slug).first()
            if category:
                # Находим все ID самой категории и всех её подкатегорий
                subcategories_ids = category.subcategories.values_list('id', flat=True)
                all_category_ids = [category.id] + list(subcategories_ids)

                # Фильтруем товары по всему списку ID (родитель + подкатегории)
                queryset = queryset.filter(category__id__in=all_category_ids)

        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.request.GET.get('category', '')
        context['current_category'] = category_slug
        context['current_search'] = self.request.GET.get('search', '')

        # --- 1. ОБЪЕКТ ТЕКУЩЕЙ КАТЕГОРИИ И ПОХОЖИЕ РАЗДЕЛЫ ---
        current_cat_obj = None
        related_categories = []
        if category_slug:
            current_cat_obj = Category.objects.filter(slug=category_slug).select_related('parent').first()
            if current_cat_obj:
                if current_cat_obj.parent:
                    # Если подкатегория -> берем сестер у того же родителя
                    related_categories = Category.objects.filter(
                        parent=current_cat_obj.parent
                    ).exclude(id=current_cat_obj.id)[:6]
                else:
                    # Если родитель -> берем его подкатегории
                    related_categories = current_cat_obj.subcategories.all()[:6]

        context['current_category_obj'] = current_cat_obj
        context['related_categories'] = related_categories

        # --- 2. ТОП-10 ПОДКАТЕГОРИЙ ДЛЯ ФУТЕРА (DEEP LINKING) ---
        context['top_subcategories'] = Category.objects.filter(
            parent__isnull=False
        ).annotate(
            active_products_count=Count('products', filter=Q(products__is_active=True))
        ).order_by('-active_products_count')[:10]

        # --- 3. СЧЕТЧИКИ ПАГИНАТОРА ---
        paginator = context.get('paginator')
        if paginator:
            total_count = paginator.count
            total_pages = paginator.num_pages

            # Логика ограничений для UX и SEO (1000+ товаров и 50+ страниц)
            context['display_count'] = "1000+" if total_count > 1000 else str(total_count)
            context['display_pages'] = "50+" if total_pages > 50 else str(total_pages)
        else:
            context['display_count'] = "0"
            context['display_pages'] = "1"

        return context