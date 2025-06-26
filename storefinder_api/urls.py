from django.urls import path, include
from .views import NearestStoresView, ProductSearchView, StoreViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'stores', StoreViewSet)

urlpatterns = [
    path('nearest-stores/', NearestStoresView.as_view(), name='nearest-stores'),
    path('product-search/', ProductSearchView.as_view(), name='product-search'),
    path('', include(router.urls)),
]