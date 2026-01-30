from datetime import timedelta

from rest_framework import viewsets
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UserSerializer, PostSerializer, CategorySerializer, SubscriberSerializer
from .models import Post, Category, Subscribers

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class PostsViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    queryset = queryset.filter(
        is_published=True,
        pub_date__lte=timezone.now(),
    ).exclude(category__is_published=False).exclude(category__isnull=True).distinct()
    serializer_class = PostSerializer
    lookup_field = 'slug'

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    queryset = queryset.filter(
        is_published=True,
    )
    serializer_class = CategorySerializer
    lookup_field = 'slug'

class SubscriberViewSet(viewsets.ModelViewSet):
    queryset = Subscribers.objects.all()
    serializer_class = SubscriberSerializer
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]
