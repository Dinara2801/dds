from django.core.management.base import BaseCommand

from dds.models import Category, Status, SubCategory, Type

class Command(BaseCommand):
    help = "Заполняет справочники типами, категориями и подкатегориями"

    def handle(self, *args, **kwargs):
        types = [
            {'name': 'Списание'},
            {'name': 'Пополнение'},
        ]

        categories = [
            {'name': 'Маркетинг', 'type_name': 'Списание'},
            {'name': 'Инфраструктура', 'type_name': 'Списание'},
            {'name': 'Продажи', 'type_name': 'Пополнение'},
            {'name': 'Инвестиции', 'type_name': 'Пополнение'},
        ]

        subcategories = [
            {'name': 'Farpost', 'category_name': 'Маркетинг'},
            {'name': 'Avito', 'category_name': 'Маркетинг'},
            {'name': 'Proxy', 'category_name': 'Инфраструктура'},
            {'name': 'VPS', 'category_name': 'Инфраструктура'},
            {'name': 'Онлайн-продажи', 'category_name': 'Продажи'},
            {'name': 'Проекты', 'category_name': 'Инвестиции'},
        ]

        statuses = [
            {'name': 'Бизнес'},
            {'name': 'Личное'},
            {'name': 'Налог'},
        ]

        for status in statuses:
            Status.objects.get_or_create(name=status['name'])
        self.stdout.write(self.style.SUCCESS('Статусы созданы'))

        for type in types:
            Type.objects.get_or_create(name=type['name'])
        self.stdout.write(self.style.SUCCESS('Типы созданы'))

        for category in categories:
            type_obj = Type.objects.get(name=category['type_name'])
            Category.objects.get_or_create(
                name=category['name'],
                type=type_obj
            )
        self.stdout.write(self.style.SUCCESS('Категории созданы'))

        for subcategory in subcategories:
            category_obj = Category.objects.get(
                name=subcategory['category_name']
            )
            SubCategory.objects.get_or_create(
                name=subcategory['name'],
                category=category_obj
            )
        self.stdout.write(self.style.SUCCESS('Подкатегории созданы'))
