from .models import Post, Category
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'email', 'is_staff']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['url', 'name', 'slug', 'id', 'is_published', 'created_at']


class PostSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = [
            'id', 'title', 'subtitle', 'text', 'slug', 'pub_date',
            'author', 'category', 'image', 'created_at',
            'is_published'
        ]
