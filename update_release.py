import os
import re


def update_sk_version(release):
    version_file = 'skvalidate/__init__.py'
    with open(version_file) as f:
        content = f.readlines()

    pattern = "(\d+\.)?(\d+\.)?(\*|\d+)"
    for i, line in enumerate(content):
        if line.startswith('__version__'):
            line = re.sub(pattern, release, line)
            content[i] = line
            break
    content = ''.join(content)
    with open(version_file, 'w') as f:
        f.write(content)


def update_changelog(release):
    input_file = 'CHANGELOG.md'
    with open(input_file) as f:
        content = f.read()
    content = content.replace('Unreleased', 'v' + release)
    content = content.replace('HEAD', 'v' + release)
    with open(input_file, 'w+') as f:
        f.write(content)


if __name__ == '__main__':
    release = os.environ.get('RELEASE', 'unreleased')
    update_sk_version(release)
    update_changelog(release)
