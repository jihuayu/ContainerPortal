import json
import os

import requests

from utils import move_image
import docker
import sys

GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
ISSUES_ID = os.environ.get('ISSUES_ID')
REPO_NAME = os.environ.get('REPO_NAME')

client = docker.from_env()

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


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python mover.py <repo>:<tag>')
        sys.exit(1)

    arg = sys.argv[1].split(':')
    repo = arg[0]
    tag = len(arg) >= 2 and arg[1] or 'latest'
    image_url = move_image(client, repo, tag)
    comment_issues(f"传输完毕，请运行：docker pull {image_url}")
    close_issues()
