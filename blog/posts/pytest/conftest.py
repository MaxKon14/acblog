from datetime import datetime, timedelta

import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from posts.models import Category, Post, Subscribers

User = get_user_model()
PASSWORD = "test_password"


@pytest.fixture
def author(django_user_model):
    """Создание пользователя - автора постов"""
    author = django_user_model.objects.create(
        username="author",
        is_superuser=True,
    )
    author.set_password(PASSWORD)
    author.save()
    return author


@pytest.fixture
def author_client(author):
    """Авторизованный API-клиент"""
    client = APIClient()
    client.force_authenticate(user=author)
    return client


@pytest.fixture
def anonymous_client():
    """Неавторизованный API-клиент"""
    return APIClient()


@pytest.fixture
def auth_header(author):
    """Получение токена авторизации"""
    token = Token.objects.create(user=author)
    return {"HTTP_AUTHORIZATION": f"Token {token.key}"}


@pytest.fixture
def category():
    """Создание категории"""
    return Category.objects.create(
        name="category",
        slug="category",
    )


@pytest.fixture
def post(category, author):
    """Создание поста"""
    post = Post.objects.create(
        title="Тестовый пост",
        subtitle="Подзаголовок",
        text="Текст поста",
        slug="test-post",
        author=author,
    )
    post.pub_date = post.pub_date - timedelta(days=1)
    post.save()
    post.category.add(category)
    return post


@pytest.fixture
def list_of_posts(author, category):
    today = datetime.today()
    all_posts = [
        Post(
            title=f"Пост {index}",
            subtitle="Подзаголовок",
            text="текст.",
            author=author,
            slug=f"slug{index}",
        )
        for index in range(settings.MAX_POSTS_ON_PAGE + 1)
    ]
    created_posts = Post.objects.bulk_create(all_posts)
    for index, post in enumerate(created_posts):
        post.pub_date = today - timedelta(days=index)
        post.save(update_fields=["pub_date"])
        post.category.add(category)

    return created_posts


@pytest.fixture
def subscriber():
    """Создание подписчика"""
    return Subscribers.objects.create(
        email="email@email.ru",
    )


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """Доступ к базе данных для всех тестов"""
    pass


@pytest.fixture
def posts_list_url():
    """URL списка постов"""
    return reverse("post-list")


@pytest.fixture
def post_detail_url(post):
    """URL деталей поста"""
    return reverse("post-detail", kwargs={"slug": post.slug})


@pytest.fixture
def categories_list_url():
    """URL списка категорий"""
    return reverse("category-list")


@pytest.fixture
def category_detail_url(category):
    """URL деталей категории"""
    return reverse("category-detail", kwargs={"slug": category.slug})


@pytest.fixture
def subscribers_list_url():
    """URL списка подписчиков"""
    return reverse("subscriber-list")


@pytest.fixture
def subscriber_detail_url(subscriber):
    """URL деталей подписчика"""
    return reverse("subscriber-detail", args=(subscriber.id,))


@pytest.fixture
def token_url():
    """URL получения токена"""
    return reverse("token")


@pytest.fixture
def email_data():
    """Email для создания подписчиков"""
    return {"email": "test@test.ru"}


@pytest.fixture
def post_data(author, category):
    """Данные для создания поста"""
    return {
        "title": "title",
        "subtitle": "subtitle",
        "text": "text",
        "category": category.id,
        "author": author.id,
    }


@pytest.fixture
def category_data():
    """Данные для создания категории"""
    return {"name": "name"}


@pytest.fixture
def unpublished_category_data():
    """Данные для создания неопубликованной категории"""
    return {"name": "name", "is_published": False}


@pytest.fixture
def token_data(author):
    """Данные для получения токена"""
    return {"username": author.username, "password": PASSWORD}
