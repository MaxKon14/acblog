from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from .views import UserViewSet, PostsViewSet, CategoryViewSet, SubscriberViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'posts', PostsViewSet, basename='post')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'subscribers', SubscriberViewSet, basename='subscriber')


urlpatterns = [
    path('', include(router.urls)),
    path('token/', obtain_auth_token, name='token'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
