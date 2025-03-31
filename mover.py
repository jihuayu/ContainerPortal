from github import comment_issues, close_issues, edit_issue_comment
from utils import move_image
import docker
import sys

client = docker.from_env()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python mover.py <repo>:<tag> [platform1,platform2,...]')
        sys.exit(1)
    data = comment_issues(f"正在拉取镜像 `{sys.argv[1]}` 请稍后")

    if len(sys.argv) >= 3:
        repo = sys.argv[1].strip()
        tag = sys.argv[2].strip()
        # 如果有第4个参数，则认为是平台列表
        platforms = sys.argv[3].strip().split(',') if len(sys.argv) >= 4 else ['linux/amd64']
    else:
        arg = sys.argv[1].strip().split(':')
        repo = arg[0]
        tag = len(arg) >= 2 and arg[1] or 'latest'
        platforms = ['linux/amd64']

    image_urls = move_image(client, repo, tag, platforms)
    
    # 构建命令输出，支持多架构
    pull_commands = []
    tag_commands = []
    for image_url in image_urls:
        pull_commands.append(f"docker pull {image_url}")
        # 为不同平台添加适当的标签
        platform_part = image_url.split('-')[-1]  # 获取平台部分
        tag_commands.append(f"docker tag {image_url} {repo}:{tag}")
    
    message = f"传输完毕，请运行以下指令拉取镜像 `{sys.argv[1]}`\n```shell\n"
    message += "\n".join(pull_commands) + "\n"
    message += "\n".join(tag_commands) + "\n```"
    
    edit_issue_comment(data.get('id'), message)
    close_issues()
