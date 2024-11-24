import pytest
from http import HTTPStatus


def test_page_access(client, public_urls):
    for url in public_urls:
        response = client.get(url)
        assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize('user_fixture, expected_status, redirect', [
    ('author_client', HTTPStatus.OK, False),
    ('reader_client', HTTPStatus.NOT_FOUND, False),
    ('client', HTTPStatus.FOUND, True)
])
def test_access_edit_delete_comments(
    user_fixture, expected_status, redirect, private_urls, request, login_url
):
    user = request.getfixturevalue(user_fixture)
    for url in private_urls:
        response = user.get(url)
        assert response.status_code == expected_status
        if redirect:
            assert response.url == f'{login_url}?next={url}'
