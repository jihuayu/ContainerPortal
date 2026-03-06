import argparse
import sys
import os

import docker
import requests

from utils import build_target_tag, move_registry_image


def parse_args():
    parser = argparse.ArgumentParser(description='Sync one image for xcr workflow dispatch.')
    parser.add_argument('--source-registry', required=True)
    parser.add_argument('--source-repo', required=True)
    parser.add_argument('--source-tag', required=True)
    parser.add_argument('--platforms', default='linux/amd64,linux/arm64')
    return parser.parse_args()


def parse_platforms(raw):
    items = []
    for item in raw.split(','):
        platform = item.strip()
        if not platform:
            continue
        parts = platform.split('/', 1)
        if len(parts) != 2 or not parts[0] or not parts[1]:
            raise ValueError(f'Invalid platform: {platform}')
        items.append(platform)
    if not items:
        raise ValueError('At least one platform is required')
    return items


def post_callback(source_registry, source_repo, source_tag, platform, aliyun_tag, success, error=None):
    callback_url = os.environ.get('XCR_CALLBACK_URL')
    callback_secret = os.environ.get('XCR_CALLBACK_SECRET')
    if not callback_url or not callback_secret:
        return

    platform_os, platform_arch = platform.split('/', 1)
    payload = {
        'source_registry': source_registry,
        'source_repo': source_repo,
        'source_tag': source_tag,
        'platform_os': platform_os,
        'platform_arch': platform_arch,
        'aliyun_tag': aliyun_tag,
        'success': success,
    }
    if error:
        payload['error'] = error[:2000]

    response = requests.post(
        callback_url,
        json=payload,
        headers={'x-sync-secret': callback_secret},
        timeout=30,
    )
    response.raise_for_status()


if __name__ == '__main__':
    args = parse_args()
    client = docker.from_env()

    try:
        platforms = parse_platforms(args.platforms)
    except ValueError as exc:
        print(str(exc))
        sys.exit(1)

    failed = False

    for platform in platforms:
        aliyun_tag = build_target_tag(args.source_registry, args.source_repo, args.source_tag, platform)
        try:
            image_urls = move_registry_image(
                client,
                args.source_registry,
                args.source_repo,
                args.source_tag,
                [platform],
            )
            print(f'Synced {image_urls[0]}')
            post_callback(
                args.source_registry,
                args.source_repo,
                args.source_tag,
                platform,
                aliyun_tag,
                True,
            )
        except Exception as exc:
            failed = True
            error = str(exc)
            print(f'Failed to sync {args.source_registry}/{args.source_repo}:{args.source_tag} {platform}: {error}')
            try:
                post_callback(
                    args.source_registry,
                    args.source_repo,
                    args.source_tag,
                    platform,
                    aliyun_tag,
                    False,
                    error,
                )
            except Exception as callback_exc:
                print(f'Callback failed for {platform}: {callback_exc}')

    if failed:
        sys.exit(1)
