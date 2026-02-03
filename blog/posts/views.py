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
    lookup_field = 'id'

class PostsViewSet(viewsets.ModelViewSet):

    serializer_class = PostSerializer
    lookup_field = 'slug'
    def get_queryset(self):
        queryset = Post.objects.all()
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(
                is_published=True,
                pub_date__lte=timezone.now(),
            ).exclude(category__is_published=False).exclude(category__isnull=True).distinct()
        return queryset


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    def get_queryset(self):
        queryset = Category.objects.all()
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(
                is_published=True,
            )
        return queryset

class SubscriberViewSet(viewsets.ModelViewSet):
    queryset = Subscribers.objects.all()
    serializer_class = SubscriberSerializer
    lookup_field = 'id'
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]
