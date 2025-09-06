from django.contrib import admin
from django.contrib.auth.models import Group

from .models import (Category, CashFlow, Status, SubCategory, Type)

admin.site.unregister(Group)


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    """Админка для модели Status."""

    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    """Админка для модели Type."""

    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Админка для модели Category."""

    list_display = ('id', 'name', 'type')
    list_filter = ('type',)
    search_fields = ('name',)


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    """Админка для модели SubCategory."""

    list_display = ('id', 'name', 'category', 'get_type')
    list_filter = ('category', 'category__type')
    search_fields = ('name',)

    def get_type(self, obj):
        """Показать тип категории у подкатегории."""
        return obj.category.type
    get_type.short_description = 'Тип'


@admin.register(CashFlow)
class CashFlowAdmin(admin.ModelAdmin):
    """Админка для модели CashFlow."""

    list_display = ('id', 'created_at', 'type', 'category',
                    'subcategory', 'amount', 'comment')
    list_filter = ('type', 'category', 'subcategory',
                   'status', ('created_at', admin.DateFieldListFilter))
    search_fields = ('comment',)
