#!/usr/bin/env python
"""Installs PyDispatcher using distutils (or setuptools/distribute)

Run:
    python setup.py install
to install the package from the source archive.
"""
import sys, os

from distutils.core import setup

if __name__ == "__main__":
    ### Now the actual set up call
    setup(
        name="PyDispatcher",
        package_dir={
            "pydispatch": "pydispatch",
        },
        packages=[
            "pydispatch",
        ],
        options={
            "sdist": {
                "use_defaults": 0,
                "force_manifest": 1,
                "formats": ["gztar"],
            },
            "bdist_rpm": {
                "group": "Libraries/Python",
                "provides": "python-dispatcher",
                "requires": "python",
            },
        },
    )
