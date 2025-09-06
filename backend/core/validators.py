from django.core.exceptions import ValidationError


def validate_cashflow(instance):
    errors = {}

    if not instance.type_id:
        errors['type'] = 'Поле "Тип" обязательно для заполнения.'
    if not instance.category_id:
        errors['category'] = 'Поле "Категория" обязательно для заполнения.'
    if not instance.subcategory_id:
        errors['subcategory'] = 'Поле "Подкатегория" обязательно для заполнения.'
    if not instance.amount:
        errors['amount'] = 'Поле "Сумма" обязательно для заполнения.'
    if instance.type_id and instance.category_id:
        if instance.category.type_id != instance.type_id:
            errors['category'] = 'Категория не относится к выбранному типу.'
            errors['type'] = 'Тип не соответствует выбранной категории.'

    if instance.category_id and instance.subcategory_id:
        if instance.subcategory.category_id != instance.category_id:
            errors['subcategory'] = 'Подкатегория не относится к выбранной категории.'
            errors['category'] = 'Категория не соответствует подкатегории.'

    if errors:
        raise ValidationError(errors)
