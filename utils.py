import os

env_var_value = os.environ.get('TARGET_REPO')
TARGET_REPO = env_var_value or 'registry.cn-hangzhou.aliyuncs.com/jihuayu/public'


def move_image(client, repo, tag, platforms=['linux/amd64']):
    for platform in platforms:
        new_tag = repo.replace('/', '-') + "-" + tag + "-" + platform.replace('/', '-')
        print(f'准备搬运 {repo}:{tag}->{new_tag} 平台: {platform}')
        image = client.images.pull(repo, tag, platform=platform)
        image.tag(TARGET_REPO, new_tag)
        client.images.push(TARGET_REPO, new_tag)
        print(f"搬运 {repo}:{tag} 平台 {platform} 成功")
    return [f'{TARGET_REPO}:{repo.replace("/", "-")}-{tag}-{platform.replace("/", "-")}' for platform in platforms]