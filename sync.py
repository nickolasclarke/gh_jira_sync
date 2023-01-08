import os
from github import Github
from jira import JIRA


def get_pr_body(github_token, owner, repo, pr_number):
    """Retrieve the body of a pull request from GitHub.

    Args:
        github_token (str): GitHub access token.
        owner (str): GitHub repository owner.
        repo (str): GitHub repository name.
        pr_number (int): Pull request number.

    Returns:
        str: Body of the pull request.
    """
    g = Github(github_token)
    repo = g.get_repo(f'{owner}/{repo}')
    pr = repo.get_pull(pr_number)
    return pr.body


def update_jira_comment(jira_api_endpoint, username, token, issue_key, pr_body):
    """Update the latest comment containing the text "from GH PR description" with the
    latest pull request body, or create a new comment if one does not exist.

    Args:
        jira_api_endpoint (str): JIRA API endpoint.
        username (str): JIRA username.
        token (str): JIRA token.
        issue_key (str): JIRA issue key.
        pr_body (str): Pull request body.
    """
    jira = JIRA(jira_api_endpoint, basic_auth=(username, token))
    comments = jira.comments(issue_key)
    latest_comment = None
    for comment in comments:
        if comment.author.name == username and 'from GH PR description' in comment.body:
            latest_comment = comment
            break

    if latest_comment:
        jira.update(latest_comment, body=pr_body)
        print(f'Comment with ID {latest_comment.id} successfully updated!')
    else:
        comment = jira.add_comment(issue_key, pr_body)
        print(f'Comment successfully created with ID {comment.id}')


def main():
    # GitHub Access Token
    GITHUB_TOKEN = '<YOUR_GITHUB_ACCESS_TOKEN>'

    # GitHub repository owner and repository name
    OWNER = '<OWNER>'
    REPO = '<REPO>'

    # Pull request number
    PR_NUMBER = <PR_NUMBER >

    # JIRA API endpoint and credentials
    JIRA_API_ENDPOINT = '<JIRA_API_ENDPOINT>'
    JIRA_USERNAME = '<JIRA_USERNAME>'
    JIRA_TOKEN = '<JIRA_TOKEN>'

    # JIRA issue key
    ISSUE_KEY = '<ISSUE_KEY>'

    # Get the pull request body
    pr_body = get_pr_body(GITHUB_TOKEN, OWNER, REPO, PR_NUMBER)

    # Update the latest comment containing the text "from GH PR description" with the
    # latest pull request body, or create a new comment if one does not exist
