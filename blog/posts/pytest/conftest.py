import pytest
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

from posts.models import Category, Post, Subscribers

User = get_user_model()

@pytest.fixture
def author(django_user_model):
    '''Создание пользователя - автора постов'''
    return django_user_model.objects.create(username='author')

@pytest.fixture
def author_client(author):
    '''Авторизованный API-клиент'''
    client = APIClient()
    client.force_authenticate(user=author)
    return client

@pytest.fixture
def anonymous_client():
    '''Неавторизованный API-клиент'''
    return APIClient()

@pytest.fixture
def auth_header(author):
    '''Получение токена авторизации'''
    token = Token.objects.create(user=author)
    return {'HTTP_AUTHORIZATION': f'Token {token.key}'}

@pytest.fixture
def category():
    '''Создание категории'''
    return Category.objects.create(
        name='category',
        slug='category',
    )

@pytest.fixture
def post(category, author):
    '''Создание поста'''
    post = Post.objects.create(
        title='Тестовый пост',
        subtitle='Подзаголовок',
        text='Текст поста',
        slug='test-post',
        author=author,
    )
    post.pub_date = post.pub_date - timedelta(seconds=1)
    post.save()
    post.category.add(category)
    return post

@pytest.fixture
def subscriber():
    '''Создание подписчика'''
    return Subscribers.objects.create(
        email='email@email.ru',
    )

@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass

@pytest.fixture
def posts_list_url():
    """URL списка постов"""
    return reverse('post-list')

@pytest.fixture
def post_detail_url(post):
    """URL деталей поста"""
    return reverse('post-detail', kwargs={'slug': post.slug})

@pytest.fixture
def categories_list_url():
    """URL списка категорий"""
    return reverse('category-list')

@pytest.fixture
def category_detail_url(category):
    """URL деталей категории"""
    return reverse('category-detail', kwargs={'slug': category.slug})

@pytest.fixture
def subscribers_list_url():
    """URL списка подписчиков"""
    return reverse('subscriber-list')

@pytest.fixture
def subscriber_detail_url(subscriber):
    """URL деталей подписчика"""
    return reverse('subscriber-detail', kwargs={'pk': subscriber.id})

@pytest.fixture
def users_list_url():
    """URL списка пользователей"""
    return reverse('user-list')

@pytest.fixture
def user_detail_url(author):
    """URL деталей пользователя"""
    return reverse('user-detail', kwargs={'pk': author.id})

@pytest.fixture
def token_url():
    """URL получения токена"""
    return reverse('api_token_auth')