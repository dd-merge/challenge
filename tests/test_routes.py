import pytest
from ..app.routes import _merge_profiles


@pytest.fixture
def profiles():
    p1 = {}
    p2 = {
        'og_repos': 1,
        'forked_repos': 5,
        'languages': ['python', 'js'],
        'language_count': '2',
        'watchers': 1000000,
        'topics': ['cat videos']
    }
    p3 = {
        'og_repos': 99,
        'forked_repos': 1,
        'languages': ['ruby', 'js'],
        'language_count': '2',
        'watchers': 10,
        'topics': ['dog videos']
    }

    return [p1, p2, p3]


def test_profile_merge_empty(profiles):
    """
    Test the profiles are merged when both profiles are empty
    """
    p1, p2, p3 = profiles

    p = _merge_profiles(p1, p1)
    assert p == {
        'original_repository_count': 0,
        'forked_repository_count': 0,
        'languages_count': 0,
        'languages': [],
        'total_watchers': 0,
        'topics': []
    }


def test_profile_merge_empty(profiles):
    """
    Test the profiles are merged if one profile is empty
    """
    p1, p2, p3 = profiles

    p = _merge_profiles(p1, p2)
    assert p['original_repository_count'] == 1
    assert p['forked_repository_count'] == 5
    assert p['languages_count'] == 2
    assert p['total_watchers'] == 1000000
    assert p['topics'] == ['cat videos']
    assert sorted(p['languages']) == ['js', 'python', ]


def test_profile_merge_and_remove_duplicates(profiles):
    """
    Test the profiles are merged correctly, and duplicate languages removed
    """
    p1, p2, p3 = profiles

    p = _merge_profiles(p2, p3)
    assert p['original_repository_count'] == 100
    assert p['forked_repository_count'] == 6
    assert p['languages_count'] == 3
    assert p['total_watchers'] == 1000010
    assert sorted(p['languages']) == ['js', 'python', 'ruby']
    assert sorted(p['topics']) == ['cat videos', 'dog videos']
