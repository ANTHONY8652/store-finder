from django.urls import path, include
from .views import NearestStoresView, ProductSearchView, StoreViewSet, CategoryViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register(r'stores', StoreViewSet)
router.register(r'category', CategoryViewSet)

urlpatterns = [
    path('nearest-stores/', NearestStoresView.as_view(), name='nearest-stores'),
    path('product-search/', ProductSearchView.as_view(), name='product-search'),
    path('', include(router.urls)),
    path('', include(router.urls)),
]