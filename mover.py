import json
import os

import requests

from github import comment_issues, close_issues, edit_issue_comment
from utils import move_image
import docker
import sys

client = docker.from_env()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python mover.py <repo>:<tag>')
        sys.exit(1)
    data = comment_issues(f"正在拉取镜像 `{sys.argv[1]}` 请稍后")
    print(data, data[id])
    arg = sys.argv[1].split(':')
    repo = arg[0]
    tag = len(arg) >= 2 and arg[1] or 'latest'
    image_url = move_image(client, repo, tag)
    edit_issue_comment(data[id],
                       f"传输完毕，请运行以下指令拉取镜像 `{sys.argv[1]}`\n"
                       f"```shell\n"
                       f"docker pull {image_url}\n"
                       f"docker tag {image_url} {sys.argv[1]}\n"
                       f"``` ")
    close_issues()
