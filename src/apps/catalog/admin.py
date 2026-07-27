from django.contrib import admin
from .models import Category, Brand, Product
from .models import ClickLog


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
            'classes': ('collapse',),  # По умолчанию свернуто
        }),
    )


@admin.register(ClickLog)
class ClickLogAdmin(admin.ModelAdmin):
    list_display = ('product', 'timestamp', 'ip_address', 'user_agent_short')

    # УБРАЛИ 'product' из list_filter, чтобы админка не выгружала все товары в память
    list_filter = ('timestamp',)

    search_fields = ('product__name', 'ip_address', 'user_agent')

    # Оптимизации производительности и памяти для логов
    list_select_related = ('product',)
    raw_id_fields = ('product',)
    show_full_result_count = False
    list_per_page = 50

    # Делаем всю панель логов доступной только для чтения
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    # Метод для красивого сокращения длинного User Agent в таблице
    def user_agent_short(self, obj):
        if obj.user_agent and len(obj.user_agent) > 50:
            return f"{obj.user_agent[:50]}..."
        return obj.user_agent

    user_agent_short.short_description = "User Agent"