from http import HTTPStatus

import pytest


@pytest.mark.parametrize(
    "url",
    [
        'categories_list_url',
        'category_detail_url',
        'posts_list_url',
        'post_detail_url',
    ]
)
def test_public_routes(anonymous_client, url, request, post, category):
    url = request.getfixturevalue(url)
    response = anonymous_client.get(url)
    print(response.content)
    assert response.status_code == HTTPStatus.OK

def test_subscribe_available_to_all(anonymous_client, subscribers_list_url, email_data):
    response = anonymous_client.post(subscribers_list_url, data=email_data, format='json')
    assert response.status_code == HTTPStatus.CREATED

def test_receiving_of_token(anonymous_client, token_url, token_data):
    response = anonymous_client.post(token_url, data=token_data, format='json')
    token = response.data['token']
    assert response.status_code == HTTPStatus.OK

@pytest.mark.parametrize(
    "url, data_fixture",
    [
        ('posts_list_url', 'post_data'),
        ('categories_list_url', 'category_data'),
    ]
)
@pytest.mark.parametrize(
    "client, expected_status",
    [
        ('author_client', HTTPStatus.CREATED),
        ('anonymous_client', HTTPStatus.UNAUTHORIZED),
    ]
)
def test_availability_for_post_and_category_adding(client, url, request, data_fixture, expected_status):
    url = request.getfixturevalue(url)
    client = request.getfixturevalue(client)
    data = None
    if data_fixture:
        data = request.getfixturevalue(data_fixture)
    response = client.post(url, data=data, format='json')
    assert response.status_code == expected_status

@pytest.mark.parametrize(
    "url",
    [
        'subscribers_list_url',
        'subscriber_detail_url',
    ]
)
@pytest.mark.parametrize(
    "client, expected_status",
    [
        ('author_client', HTTPStatus.OK),
        ('anonymous_client', HTTPStatus.UNAUTHORIZED),
    ]
)
def test_availability_for_subscribers_list_and_detail(client, url, request, expected_status):
    url = request.getfixturevalue(url)
    client = request.getfixturevalue(client)
    response = client.get(url, format='json')
    assert response.status_code == expected_status
