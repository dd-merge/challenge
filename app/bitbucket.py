import requests

BITBUCKET_API_URL = 'https://api.bitbucket.org/2.0'
WATCHERS_RESOURCE = 'repositories/{}/{}/watchers'
REPOSITORIES_RESOURCE = 'repositories/{}'


def _bitbucket_request(resource, fields='+*'):
    """
    Prepares and sends a REST request against the BitBucket API
    Returns the json payload on a successful 200 request,
    an empty dictionary if a 404 is received, or raises an Exception if neither of those is true
    """
    r = requests.get('{}/{}'.format(BITBUCKET_API_URL, resource),
                     params={'fields': fields})

    if r.status_code == 200:
        return r.json()
    if r.status_code == 404:
        return {}

    print(r.status_code, r.json())

    raise Exception('Query failed, status code {}'.format(r.status_code))


def bitbucket_get_profile(team):
    """
    Generates the profile of a specified team in BitBucket.

    Args:
        team (str): Name of BitBucket team

    Returns:
        dict: Returns team profile as a dictionary, or an empty dictionary if team was not found

    Raises:
        Exception: An error occurred accessing BitBucket
    """
    r = _bitbucket_request(REPOSITORIES_RESOURCE.format(team),
                           'values.name,values.parent,values.language,size')

    # Return empty profile if team not found
    if not r:
        return {}

    repos = r.get('values')
    total_repos = r.get('size')
    forked_repos = len([repo for repo in repos if repo.get('parent')])
    og_repos = total_repos - forked_repos
    languages = list(
        set([repo.get('language') for repo in repos if repo.get('language')]))

    watchers = 0
    for repo in repos:
        watchers += _bitbucket_request(
            WATCHERS_RESOURCE.format(team, repo.get('name')),
            'size').get('size', 0)

    return {
        'forked_repos': forked_repos,
        'og_repos': og_repos,
        'languages': languages,
        'language_count': len(languages),
        'watchers': watchers,
    }
