from http import HTTPStatus

import pytest

from posts.models import (
    MAX_LENGTH_OF_CATEGORY_NAME,
    MAX_LENGTH_OF_SUBTITLE,
    MAX_LENGTH_OF_TITLE,
)


@pytest.mark.parametrize("missing_field", ["title", "text"])
def test_post_creation_requires_fields(
    author_client, posts_list_url, post_data, missing_field
):
    data = post_data.copy()
    data.pop(missing_field)
    response = author_client.post(posts_list_url, data, format="json")
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert missing_field in response.data


def test_post_title_max_length_violation(author_client, posts_list_url, post_data):
    data = post_data.copy()
    data["title"] = "A" * (MAX_LENGTH_OF_TITLE + 1)
    response = author_client.post(posts_list_url, data, format="json")
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert "title" in response.data


def test_post_subtitle_max_length_violation(author_client, posts_list_url, post_data):
    data = post_data.copy()
    data["subtitle"] = "B" * (MAX_LENGTH_OF_SUBTITLE + 1)
    response = author_client.post(posts_list_url, data, format="json")
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert "subtitle" in response.data


def test_category_name_max_length_violation(author_client, categories_list_url):
    data = {}
    data["name"] = "C" * (MAX_LENGTH_OF_CATEGORY_NAME + 1)
    response = author_client.post(categories_list_url, data, format="json")
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert "name" in response.data


def test_post_invalid_category_id(author_client, posts_list_url, post_data):
    data = post_data.copy()
    data["category_ids"] = [999999]
    response = author_client.post(posts_list_url, data, format="json")
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert "category" in str(response.data).lower()


@pytest.mark.parametrize(
    "invalid_email",
    [
        "",
        "no-at-sign",
        "user@",
        "@domain.ru",
        "user@.ru",
        "user@domain",
        "user@-domain.com",
        "user.name@domain..com",
    ],
)
def test_subscriber_invalid_email_formats(
    anonymous_client, subscribers_list_url, invalid_email
):
    data = {"email": invalid_email}
    response = anonymous_client.post(subscribers_list_url, data, format="json")
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert "email" in str(response.data).lower()


def test_patch_invalid_category_id(author_client, post_detail_url):
    invalid_data = {"category_ids": [999999]}
    response = author_client.patch(post_detail_url, invalid_data, format="json")
    assert response.status_code == HTTPStatus.BAD_REQUEST
