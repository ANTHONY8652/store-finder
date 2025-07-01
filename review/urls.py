from .views import ReviewViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'', ReviewViewSet)


urlpatterns = [
    path('', include(router.urls)),
]