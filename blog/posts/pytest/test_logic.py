from http import HTTPStatus

from pytils.translit import slugify
from posts.models import Post, Category, Subscribers


def test_auto_post_slug_generation(anonymous_client, author_client, posts_list_url, post_data):
    posts_before = Post.objects.count()
    author_client.post(posts_list_url, data=post_data, format='json')
    posts_after = Post.objects.count()
    assert posts_after == posts_before + 1
    assert Post.objects.get().slug == slugify(post_data['title'])

def test_auto_category_slug_generation(anonymous_client, author_client, categories_list_url, category_data):
    categories_before = Category.objects.count()
    author_client.post(categories_list_url, data=category_data, format='json')
    categories_after = Category.objects.count()
    assert categories_after == categories_before + 1
    assert Category.objects.get().slug == slugify(category_data['name'])

def test_creating_post_with_existing_slug(anonymous_client, author_client, posts_list_url, post, category):
    posts_before = Post.objects.count()
    data = {
        'title': post.title,
        'subtitle': post.subtitle,
        'text': post.text,
        'category': category.id,
        'author': post.author.id,
        'slug' : post.slug
    }
    response = author_client.post(posts_list_url, data=data, format='json')
    posts_after = Post.objects.count()
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert posts_after == posts_before

def test_subscriber_email_must_be_unique(anonymous_client, subscribers_list_url, request, email_data):
    anonymous_client.post(subscribers_list_url, data=email_data, format='json')
    subs_before = Subscribers.objects.count()
    response = anonymous_client.post(subscribers_list_url, data=email_data, format='json')
    subs_after = Subscribers.objects.count()
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert subs_after == subs_before


