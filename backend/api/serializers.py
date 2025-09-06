from rest_framework import serializers

from core.validators import validate_cashflow
from dds.models import Status, Type, Category, SubCategory, CashFlow


class StatusSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Status."""

    class Meta:
        model = Status
        fields = '__all__'


class TypeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Type."""

    class Meta:
        model = Type
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Category.

    Включает проверку уникальности названия категории для типа.
    """
    type = serializers.StringRelatedField()

    class Meta:
        model = Category
        fields = '__all__'

    def validate(self, validated_data):
        """Валидация уникальности имени категории для выбранного типа."""
        type_obj = self.context['view'].get_type()
        name = validated_data.get('name')

        if Category.objects.filter(name=name, type=type_obj).exists():
            raise serializers.ValidationError(
                f'Категория "{name}" уже существует для типа "{type_obj}".'
            )

        return validated_data


class SubCategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели SubCategory.

    Включает проверку уникальности названия подкатегории для категории.
    """
    category = serializers.StringRelatedField()

    class Meta:
        model = SubCategory
        fields = '__all__'

    def validate(self, validated_data):
        """"Валидация уникальности подкатегории внутри категории."""
        category_obj = self.context['view'].get_category()
        name = validated_data.get('name')

        if SubCategory.objects.filter(
            name=name,
            category=category_obj
        ).exists():
            raise serializers.ValidationError(
                f'Подкатегория "{name}" уже существует '
                f'для категории "{category_obj}".'
            )

        return validated_data


class CashFlowSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели CashFlow.

    Включает в себя проверку логической связи типа, категории и подкатегории.
    """
    type = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Type.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Category.objects.all()
    )
    subcategory = serializers.SlugRelatedField(
        slug_field='name',
        queryset=SubCategory.objects.all()
    )
    status = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Status.objects.all()
    )

    class Meta:
        model = CashFlow
        fields = '__all__'

    def validate(self, data):
        instance = CashFlow(**data)
        validate_cashflow(instance)
        return data

    def get_status(self, obj):
        return obj.get_status_display()
