from .models import Post, Category, Subscribers
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'email', 'is_staff']


class CategorySerializer(serializers.ModelSerializer):
    posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    url = serializers.HyperlinkedIdentityField(
        view_name='post-detail',
        lookup_field='slug',
    )
    class Meta:
        model = Category
        fields = ['url', 'name', 'slug', 'id', 'is_published', 'created_at', 'posts']


class PostSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True, read_only=True)

    category_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Category.objects.all(),
        source='category',
        write_only=True,
        required=False
    )
    url = serializers.HyperlinkedIdentityField(
        view_name='post-detail',
        lookup_field='slug',
    )
    class Meta:
        model = Post
        fields = [
            'url', 'id', 'title', 'subtitle', 'text', 'slug', 'pub_date',
            'author', 'category', 'category_ids', 'image', 'created_at', 'is_published'
        ]

class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscribers
        fields = ['url', 'email', 'id', 'is_active', 'subscribed_at']
        read_only_fields = ['is_active', 'subscribed_at']