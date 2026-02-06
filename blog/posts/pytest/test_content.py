from datetime import timedelta

from django.conf import settings
from django.urls import reverse
from django.utils import timezone


def test_count_posts_on_page(anonymous_client, list_of_posts, posts_list_url):
    response = anonymous_client.get(posts_list_url)
    response_json = response.json()
    results = response_json["results"]
    assert len(results) == settings.MAX_POSTS_ON_PAGE


def test_posts_order_on_page(anonymous_client, list_of_posts, posts_list_url):
    response = anonymous_client.get(posts_list_url)
    response_json = response.json()
    results = response_json["results"]
    all_dates = [post["pub_date"] for post in results]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


def test_only_published_posts_in_list(
    anonymous_client, author_client, posts_list_url, post_detail_url
):
    response = anonymous_client.get(posts_list_url)
    response_json = response.json()
    results = response_json["results"]
    assert len(results) == 1
    author_client.patch(
        post_detail_url,
        data={
            "is_published": False,
        },
        format="json",
    )
    response = anonymous_client.get(posts_list_url)
    response_json = response.json()
    results = response_json["results"]
    assert len(results) == 0


def test_only_posts_with_published_categories_in_list(
    posts_list_url,
    post,
    anonymous_client,
    author_client,
    categories_list_url,
    unpublished_category_data,
):
    response = anonymous_client.get(posts_list_url)
    response_json = response.json()
    results = response_json["results"]
    assert len(results) == 1
    new_category_response = author_client.post(
        categories_list_url, data=unpublished_category_data, format="json"
    )
    new_category_id = new_category_response.json()["id"]
    new_category_slug = new_category_response.json()["slug"]
    print(new_category_slug)
    post.category.add(new_category_id)
    response = anonymous_client.get(posts_list_url)
    response_json = response.json()
    results = response_json["results"]
    assert len(results) == 0
    author_client.patch(
        reverse("category-detail", kwargs={"slug": new_category_slug}),
        data={
            "is_published": True,
        },
        format="json",
    )
    response = anonymous_client.get(posts_list_url)
    response_json = response.json()
    results = response_json["results"]
    assert len(results) == 1


def test_only_posts_valid_pub_date_in_list(
    anonymous_client, author_client, posts_list_url, post_detail_url
):
    response = anonymous_client.get(posts_list_url)
    response_json = response.json()
    results = response_json["results"]
    assert len(results) == 1
    author_client.patch(
        post_detail_url,
        data={
            "pub_date": timezone.now() + timedelta(days=1),
        },
        format="json",
    )
    response = anonymous_client.get(posts_list_url)
    response_json = response.json()
    results = response_json["results"]
    assert len(results) == 0
