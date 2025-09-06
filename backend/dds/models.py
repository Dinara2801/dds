from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from smart_selects.db_fields import ChainedForeignKey

from core.models import AbstractName
from core.validators import validate_cashflow


class Status(AbstractName):
    """Модель статуса движения денежных средств (ДДС)."""

    class Meta(AbstractName.Meta):
        verbose_name = 'статус'
        verbose_name_plural = 'Статусы'


class Type(AbstractName):
    """Модель типа движения денежных средств (ДДС)."""

    class Meta(AbstractName.Meta):
        verbose_name = 'тип'
        verbose_name_plural = 'Типы'


class Category(AbstractName):
    """Модель категории ДДС, связанной с типом."""

    type = models.ForeignKey(
        Type,
        on_delete=models.CASCADE,
        related_name='categories',
        verbose_name='Тип'
    )

    class Meta(AbstractName.Meta):
        constraints = (
            models.UniqueConstraint(
                fields=('name', 'type'),
                name='unique_name_type'
            ),
        )
        verbose_name = 'категорию'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class SubCategory(AbstractName):
    """Модель подкатегории ДДС, связанной с категорией."""

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='subcategories',
        verbose_name='Категория'
    )

    class Meta(AbstractName.Meta):
        constraints = (
            models.UniqueConstraint(
                fields=('name', 'category'),
                name='unique_name_category'
            ),
        )
        verbose_name = 'подкатегорию'
        verbose_name_plural = 'Подкатегории'

    def __str__(self):
        return self.name


class CashFlow(models.Model):
    """Модель записи движения денежных средств (ДДС)."""

    created_at = models.DateField(
        default=timezone.now,
        verbose_name='Дата создания записи',
    )

    type = models.ForeignKey(
        Type,
        on_delete=models.PROTECT,
        verbose_name='Тип'
    )

    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        verbose_name='Статус'
    )

    category = ChainedForeignKey(
        'dds.Category',
        chained_field='type',
        chained_model_field='type',
        show_all=False,
        auto_choose=True,
        sort=True,
        on_delete=models.PROTECT,
        verbose_name='Категория'
    )

    subcategory = ChainedForeignKey(
        'dds.SubCategory',
        chained_field='category',
        chained_model_field='category',
        show_all=False,
        auto_choose=True,
        sort=True,
        on_delete=models.PROTECT,
        verbose_name='Подкатегория'
    )

    amount = models.PositiveIntegerField(
        'Сумма в рублях',
        validators=(MinValueValidator(0),)
    )

    comment = models.TextField(
        'Комментарий',
        blank=True
    )

    class Meta:
        ordering = ('-created_at',)
        default_related_name = 'cashflows'
        verbose_name = 'запись ДДС'
        verbose_name_plural = 'Записи ДДС'

    def clean(self):
        validate_cashflow(self)

    def __str__(self):
        return (f'{self.created_at} | {self.type} | '
                f'{self.category} / {self.subcategory} | {self.amount}')
