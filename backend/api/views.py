from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.pagination import LimitOffsetPagination

from .serializers import (
    StatusSerializer, TypeSerializer, CategorySerializer,
    SubCategorySerializer, CashFlowSerializer
)
from dds.models import (Category, CashFlow, Status, SubCategory, Type)


class StatusViewSet(viewsets.ModelViewSet):
    """ViewSet для создания, удаления, редактирования и чтения cтатусов."""

    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TypeViewSet(viewsets.ModelViewSet):
    """ViewSet для создания, удаления, редактирования и чтения типа."""

    queryset = Type.objects.all()
    serializer_class = TypeSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class CategoryViewSet(viewsets.ModelViewSet):
    """ViewSet для создания, удаления, редактирования и чтения категории."""

    serializer_class = CategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('type',)
    search_fields = ('name',)

    def get_type(self):
        """Получить объект типа операции на основе параметров URL."""
        return get_object_or_404(Type, pk=self.kwargs.get('type_id'))

    def perform_create(self, serializer):
        """Создание категории."""
        serializer.save(type=self.get_type())

    def get_queryset(self):
        """Получить категории для viewset."""
        return self.get_type().categories.all()


class SubCategoryViewSet(viewsets.ModelViewSet):
    """ViewSet для создания, удаления, редактирования и чтения подкатегорий."""

    serializer_class = SubCategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('category',)
    search_fields = ('name',)

    def get_category(self):
        """Получить объект категории на основе параметров URL."""
        return get_object_or_404(
            Category,
            pk=self.kwargs.get('category_id'),
            type__id=self.kwargs.get('type_id'),
        )

    def perform_create(self, serializer) -> None:
        """Создание подкатегории."""
        serializer.save(category=self.get_category())

    def get_queryset(self):
        """Получить подкатегории для viewset."""
        return self.get_category().subcategories.all()


class CashFlowViewSet(viewsets.ModelViewSet):
    """ViewSet для создания, удаления, редактирования и чтения записей ДДС."""

    queryset = CashFlow.objects.all().select_related(
        'status', 'type', 'category', 'subcategory'
    ).order_by('-created_at')
    serializer_class = CashFlowSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (
        DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter
    )
    filterset_fields = (
        'status', 'type', 'category', 'subcategory', 'created_at'
    )
    search_fields = ('comment',)
    ordering_fields = ('created_at', 'amount')
