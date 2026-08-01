from django.contrib import admin
from django.core.paginator import Paginator
from django.db import connection
from .models import Category, Brand, Product, ClickLog


class LargeTablePaginator(Paginator):
    """
    Безопасный пагинатор для больших таблиц.
    Берет примерную оценку из статистики Postgres (pg_class),
    а при любой ошибке автоматически откатывается на стандартный подсчет.
    """

    def _get_count(self):
        try:
            if hasattr(self.object_list, 'query') and not self.object_list.query.where:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT reltuples::bigint FROM pg_class WHERE relname = %s",
                        [self.object_list.model._meta.db_table]
                    )
                    row = cursor.fetchone()
                    if row and row[0] is not None and int(row[0]) >= 0:
                        return int(row[0])
        except Exception:
            pass  # При любой ошибке просто переходим к фоллбэку

        return super().count

    count = property(_get_count)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'parent')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Что показываем в таблице всех товаров
    list_display = ('name', 'category', 'brand', 'price', 'is_active', 'created_at')

    # Быстрые фильтры справа
    list_filter = ('is_active', 'category', 'brand', 'created_at')

    # Поиск по имени и описанию товара
    search_fields = ('name', 'description')

    # Автоматический slug
    prepopulated_fields = {'slug': ('name',)}

    # Поля только для чтения
    readonly_fields = ('created_at', 'updated_at')

    # Оптимизация запросов к БД в списочном виде
    list_select_related = ('category', 'brand')

    # --- ОПТИМИЗАЦИЯ ДЛЯ БОЛЬШИХ ТАБЛИЦ ---
    show_full_result_count = False  # Отключает честный COUNT(*) по всей базе при фильтрации
    paginator = LargeTablePaginator  # Безопасная быстрая пагинация

    # Группируем поля на странице редактирования товара для красоты
    fieldsets = (
        ('General Info', {
            'fields': ('name', 'slug', 'category', 'brand', 'description', 'price', 'is_active')
        }),
        ('Affiliate & Links', {
            'fields': ('original_url', 'affiliate_url', 'image_url')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )


@admin.register(ClickLog)
class ClickLogAdmin(admin.ModelAdmin):
    list_display = ('product', 'timestamp', 'ip_address', 'user_agent_short')
    list_filter = ('timestamp',)
    search_fields = ('product__name', 'ip_address', 'user_agent')

    list_select_related = ('product',)
    raw_id_fields = ('product',)
    show_full_result_count = False
    list_per_page = 50

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def user_agent_short(self, obj):
        if obj.user_agent and len(obj.user_agent) > 50:
            return f"{obj.user_agent[:50]}..."
        return obj.user_agent

    user_agent_short.short_description = "User Agent"