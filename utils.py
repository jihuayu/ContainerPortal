import os

env_var_value = os.environ.get('TARGET_REPO')
TARGET_REPO = env_var_value or 'registry.cn-hangzhou.aliyuncs.com/jihuayu/public'


def build_source_image(source_registry, source_repo):
    if source_registry == 'docker.io':
        return source_repo
    return f'{source_registry}/{source_repo}'


def build_target_tag(source_registry, source_repo, source_tag, platform):
    platform_os, platform_arch = platform.split('/', 1)
    repo_part = source_repo.replace('/', '-')
    return f'{source_registry}-{repo_part}-{source_tag}-{platform_os}-{platform_arch}'


def move_registry_image(client, source_registry, source_repo, source_tag, platforms=['linux/amd64']):
    source_image = build_source_image(source_registry, source_repo)
    image_urls = []

    for platform in platforms:
        new_tag = build_target_tag(source_registry, source_repo, source_tag, platform)
        print(f'准备搬运 {source_image}:{source_tag}->{new_tag} 平台: {platform}')
        image = client.images.pull(source_image, source_tag, platform=platform)
        image.tag(TARGET_REPO, new_tag)
        client.images.push(TARGET_REPO, new_tag)
        print(f'搬运 {source_image}:{source_tag} 平台 {platform} 成功')
        image_urls.append(f'{TARGET_REPO}:{new_tag}')

    return image_urls


def move_image(client, repo, tag, platforms=['linux/amd64']):
    for platform in platforms:
        new_tag = repo.replace('/', '-') + "-" + tag + "-" + platform.replace('/', '-')
        print(f'准备搬运 {repo}:{tag}->{new_tag} 平台: {platform}')
        image = client.images.pull(repo, tag, platform=platform)
        image.tag(TARGET_REPO, new_tag)
        client.images.push(TARGET_REPO, new_tag)
        print(f"搬运 {repo}:{tag} 平台 {platform} 成功")
    return [f'{TARGET_REPO}:{repo.replace("/", "-")}-{tag}-{platform.replace("/", "-")}' for platform in platforms]
