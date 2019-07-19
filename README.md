# Coding Challenge App

A skeleton flask app to use for a coding challenge.

## Running the code

### Generate a GitHub Personal Access Token

https://developer.github.com/v4/guides/forming-calls/#authenticating-with-graphql

The following scopes should be added:
```
user
public_repo
repo
repo_deployment
repo:status
read:repo_hook
read:org
read:public_key
read:gpg_key
```

### Build the Docker image

```
docker build -t dd-challenge .
```

### Spin up the image

```
docker run -it -p 5000:5000 -e GITHUB_API_TOKEN=<GitHub API Token> dd-challenge
```

### Making Requests

```
curl -i "http://localhost:5000/profile/?org=mailchimp&team=mailchimp"
```

### Run tests

```
docker run -it --entrypoint="pytest" dd-challenge
```


## What'd I'd like to improve on...

- GitHub's GraphQL API has been problematic, especially when working with 
organizations that have their OAuth App permissions locked down (i.e. mailchimp, 
pygame).  Accessing organizations that are not locked down (i.e. github) on the
other hand is fine. 
- Pagination is not currently supported.  That still needs to be fleshed out, 
or switch to a library like `python-bitbucket` that supports it.
- Test coverage is a little sparse.  The lower level functions have test 
coverage, but the end to end functionality is untested
- Error handling could be expanded.  Network errors or GH/BB API errors could
be protected against and better reported
- Using a package like Flask-RESTPlus would have helped with documentation
- Topics / Languages could use sorting, case-insensitive duplicate removal
