import os
from requests import Request, Session

ORG_QUERY = '''
query ($org: String!) {
  organization(login: $org) {
    ogRepos: repositories(isFork: false, first: 0) {
      totalCount
    }
    repositories(first: 50) {
      totalCount
      nodes {
        watchers(first: 0) {
          totalCount
        }
        languages(first: 10) {
          totalCount
          nodes {
            name
          }
        }
        repositoryTopics(first: 10) {
          nodes {
            topic {
              name
            }
          }
        }
      }
    }
  }
}
'''

GITHUB_API_URL = 'https://api.github.com/graphql'
GITHUB_HEADERS = {
    'Authorization': 'token %s' % os.getenv('GITHUB_API_TOKEN'),
    'User-Agent': 'python-requests/2.22.0',
}


def _github_query(query, variables):
    """
    Prepares and sends a GraphQL query against the GitHub API Returns the json payload on a successful 200 request,
    and empty dictionary if the NOT_FOUND error is returned, or raises an Exception if neither of those is true
    """
    # Manually creating our request to prevent the 'Accept' header from being automatically set by requests.post
    # Related to an issue with the GitHub GraphQL API:  https://github.com/google/go-github/issues/1037
    s = Session()
    request = Request('POST',
                      GITHUB_API_URL,
                      json={
                          'query': query,
                          'variables': variables
                      },
                      headers=GITHUB_HEADERS)
    prepped = request.prepare()
    r = s.send(prepped)

    if r.status_code == 200:
        data = r.json()
        if data.get('errors'):
            error_type = data.get('errors')[0].get('type')
            if error_type == "NOT_FOUND":
                return {}
        else:
            return data
    raise Exception('Query failed, status code {}'.format(r.status_code))


def github_get_profile(organization):
    """
    Generates the profile of a specified organization in GitHub.

    Args:
        organization (str): Name of GitHub organization

    Returns:
        dict: Returns organization profile as a dictionary, or an empty dictionary if organization was not found

    Raises:
        Exception: An error occurred accessing GitHub
    """

    r = _github_query(ORG_QUERY, {'org': organization})

    # Return empty profile if org not found
    if not r:
        return {}

    org = r['data']['organization']
    repos = org['repositories']['nodes']
    og_repos = org['ogRepos']['totalCount']
    forked_repos = org['repositories']['totalCount'] - og_repos
    language_lists = [repo['languages']['nodes'] for repo in repos]
    languages = list(
        set([
            lang['name'] for lang_list in language_lists for lang in lang_list
        ]))
    topic_lists = [repo['repositoryTopics']['nodes'] for repo in repos]
    topics = [
        topic['topic']['name'] for topic_list in topic_lists
        for topic in topic_list
    ]
    watchers = sum([repo['watchers']['totalCount'] for repo in repos])

    return {
        'forked_repos': forked_repos,
        'og_repos': og_repos,
        'languages': languages,
        'language_count': len(languages),
        'watchers': watchers,
        'topics': list(set(topics)),
    }
