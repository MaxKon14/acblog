import pytest
from django.utils import timezone


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
    print(post.pub_date)
    print(timezone.now())
    assert response.status_code == 200
