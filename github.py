import json
import os

import requests

GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
ISSUES_ID = os.environ.get('ISSUES_ID')
REPO_NAME = os.environ.get('REPO_NAME')


def comment_issues(comment):
    if GITHUB_TOKEN and ISSUES_ID and REPO_NAME:
        url = f'https://api.github.com/repos/{REPO_NAME}/issues/{ISSUES_ID}/comments'
        headers = {
            'Authorization': f'token {GITHUB_TOKEN}',
            'Accept': 'application/vnd.github.v3+json'
        }
        data = {
            'body': comment
        }
        response = requests.post(url, headers=headers, data=json.dumps(data))
        return response.json()


def edit_issue_comment(comment_id, comment):
    print(comment_id)
    if GITHUB_TOKEN and ISSUES_ID and REPO_NAME:
        url = f'https://api.github.com/repos/{REPO_NAME}/issues/{ISSUES_ID}/comments/{comment_id}'
        headers = {
            'Authorization': f'token {GITHUB_TOKEN}',
            'Accept': 'application/vnd.github.v3+json'
        }
        data = {
            'body': comment
        }
        response = requests.patch(url, headers=headers, data=json.dumps(data))
        print(response.json())


def close_issues():
    if GITHUB_TOKEN and ISSUES_ID and REPO_NAME:
        url = f'https://api.github.com/repos/{REPO_NAME}/issues/{ISSUES_ID}'
        headers = {
            'Authorization': f'token {GITHUB_TOKEN}',
            'Accept': 'application/vnd.github.v3+json'
        }
        data = {
            'state': 'closed'
        }
        response = requests.patch(url, headers=headers, data=json.dumps(data))
        return response.json()
