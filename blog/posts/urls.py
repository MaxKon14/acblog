from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, PostsViewSet, CategoryViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'posts', PostsViewSet)
router.register(r'categories', CategoryViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]