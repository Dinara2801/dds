from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    StatusViewSet, TypeViewSet, CategoryViewSet,
    SubCategoryViewSet, CashFlowViewSet
)

router = DefaultRouter()
router.register(
    'statuses',
    StatusViewSet,
    basename='statuses'
)
router.register(
    'types',
    TypeViewSet,
    basename='types'
)
router.register(
    r'types/(?P<type_id>\d+)/categories',
    CategoryViewSet,
    basename='categories',
)
router.register(
    r'types/(?P<type_id>\d+)/categories/(?P<category_id>\d+)/subcategories',
    SubCategoryViewSet,
    basename='subcategories',
)
router.register(
    'cashflows',
    CashFlowViewSet,
    basename='cashflows'
)

urlpatterns = [
    path('', include(router.urls)),
]
