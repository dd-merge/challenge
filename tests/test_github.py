from ..app.github import _github_query, GITHUB_API_URL, ORG_QUERY


def test_github_not_found(requests_mock):
    """
    Test an empty profile is returned if org not found
    """
    requests_mock.register_uri('POST', GITHUB_API_URL, json={'errors': [{'type': 'NOT_FOUND'}]}, status_code=200)
    r = _github_query(ORG_QUERY, {'org': 'github'})

    assert r == {}
