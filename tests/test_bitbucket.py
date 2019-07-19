from ..app.bitbucket import _bitbucket_request, REPOSITORIES_RESOURCE


def test_bitbucket_not_found(requests_mock):
    """
    Test an empty profile is returned if team not found
    """
    team = 'github'
    requests_mock.register_uri('GET', 'https://api.bitbucket.org/2.0/repositories/github?fields=%2B%2A', status_code=404)
    r = _bitbucket_request(REPOSITORIES_RESOURCE.format(team))

    assert r == {}
