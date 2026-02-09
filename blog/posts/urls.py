from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, PostsViewSet, SubscriberViewSet, UserViewSet

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"posts", PostsViewSet, basename="post")
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"subscribers", SubscriberViewSet, basename="subscriber")


urlpatterns = [
    path("", include(router.urls)),
    path("token/", obtain_auth_token, name="token"),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
