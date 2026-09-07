"""Suppress tests which test features newer than the running interpreter"""
import sys
import re

TAG_FINDER = re.compile(r'py(?P<major>\d+)_(?P<minor>\d+)\.py[a-z]*$')


def pytest_ignore_collect(collection_path, config):
    match = TAG_FINDER.search(collection_path.name)
    if match:
        required_major = int(match.group('major'))
        if required_major < sys.version_info.major:
            return True
        elif required_major > sys.version_info.major:
            return False
        required_minor = int(match.group('minor'))
        if required_minor > sys.version_info.minor:
            return True

    return False
