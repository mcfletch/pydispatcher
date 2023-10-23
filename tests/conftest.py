"""Suppress tests which test python3 specific features when running on python2"""
import sys, re, os

TAG_FINDER = re.compile(r'py(?P<major>\d+)_(?P<minor>\d+)\.py[a-z]*$')


def pytest_ignore_collect(path, config):
    match = TAG_FINDER.search(os.path.basename(path))
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
