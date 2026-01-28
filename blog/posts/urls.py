from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from .views import UserViewSet, PostsViewSet, CategoryViewSet, SubscriberViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'posts', PostsViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'subscribers', SubscriberViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('token/', obtain_auth_token),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]