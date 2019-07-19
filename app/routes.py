import logging
import flask
from flask import Response, jsonify, request
from .bitbucket import bitbucket_get_profile
from .github import github_get_profile

app = flask.Flask("user_profiles_api")
logger = flask.logging.create_logger(app)
logger.setLevel(logging.INFO)


def _merge_profiles(p1, p2):
    """
    Merge two profiles together.  If a field is missing, it is treated as a 0 or empty list.  Duplicate entries are
    removed from languages and topics
    """
    languages = list(set(p1.get('languages', []) + p2.get('languages', [])))
    topics = list(set(p1.get('topics', []) + p2.get('topics', [])))

    return {
        'original_repository_count': p1.get('og_repos', 0) + p2.get('og_repos', 0),
        'forked_repository_count': p1.get('forked_repos', 0) + p2.get('forked_repos', 0),
        'languages_count': len(languages),
        'languages': languages,
        'total_watchers': p1.get('watchers', 0) + p2.get('watchers', 0),
        'topics': topics
    }


@app.route("/health-check", methods=["GET"])
def health_check():
    """
    Endpoint to health check API
    """
    app.logger.info("Health Check!")
    return Response("All Good!", status=200)


@app.route('/profile/', methods=["GET"])
def get_profile():
    """
        Endpoint to request the merged profile from a GitHub organization and BitBucket team
        ---
        parameters:
          - name: org
            in: query
            type: string
            required: false
            description: The GitHub organization
          - name: team
            in: query
            type: string
            required: false
            description: The BitBucket team
        responses:
          500:
            description: An error occured while accessing the BitBucket or GitHub services
          400:
            description: Missing an org or team parameter
          200:
            description: Merged profile from a GitHub org and BitBucket team
            schema:
              original_repository_count:
                type: integer
                description: Combined number of original repositories
              forked_repository_count:
                type: integer
                description: Combined number of forked repositories
              languages_count:
                type: integer
                description: Combined number of languages
              languages:
                type: list
                items:
                    type: string
                    description: All programming languages used across all repositories
              total_watchers:
                type: integer
                description: Total number of watchers across all repositories
              topics:
                type: list
                items:
                    type: string
                    description: All topics across all repositories

        """

    org = request.args.get('org')
    team = request.args.get('team')

    if not org and not team:
        return jsonify(
            {'error': 'Need at least one organization or team name!'}), 400

    gh = {}
    if org:
        try:
            gh = github_get_profile(org)
        except Exception:
            return jsonify({'error': 'Error accessing GitHub API'}), 500

        if not gh:
            return jsonify({'error': 'GitHub org not found'}), 404

    bb = {}
    if team:
        try:
            bb = bitbucket_get_profile(team)
        except Exception:
            return jsonify({'error': 'Error accessing BitBucket API'}), 500

        if not bb:
            return jsonify({'error': 'BitBucket team not found'}), 404

    return jsonify(_merge_profiles(gh, bb))
