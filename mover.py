import os

from utils import move_image
import docker
import sys
from github import Github, Auth

GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
ISSUES_ID = os.environ.get('ISSUES_ID')
REPO_NAME = os.environ.get('REPO_NAME')

if GITHUB_TOKEN:
    auth = Auth.Token
    g = Github(GITHUB_TOKEN)

client = docker.from_env()


def comment_issues(comment):
    if g and ISSUES_ID:
        repo = g.get_repo(REPO_NAME)
        repo.get_issue(int(ISSUES_ID)).create_comment(comment)


def close_issues():
    if g and ISSUES_ID:
        repo = g.get_repo(REPO_NAME)
        repo.get_issue(int(ISSUES_ID)).edit(state='closed')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python mover.py <repo>:<tag>')
        sys.exit(1)

    arg = sys.argv[1].split('|')
    repo = arg[0]
    tag = len(arg) >= 2 and arg[1] or 'latest'
    image_url = move_image(client, repo, tag)
    comment_issues(f"传输完毕，请运行：docker pull {image_url}")
    close_issues()
