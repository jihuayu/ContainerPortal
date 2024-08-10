import json
from typing import Dict, List
import docker

from utils import move_image

with open('config.json', 'r') as file:
    data: Dict[str, List[str]] = json.load(file)

client = docker.from_env()

count = 0

for repo, tags in data.items():
    for tag in tags:
        try:
            move_image(client, repo, tag)
            count = count + 1
        except Exception as e:
            print(f'搬运 {repo}:{tag} 时发生错误：', e)

print("搬运完工，总计搬运镜像数量: ", count)
