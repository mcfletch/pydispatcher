#!/usr/bin/env python
"""Installs PyDispatcher using distutils

Run:
    python setup.py install
to install the package from the source archive.
"""
from setuptools import setup
import os
from sys import hexversion
if hexversion >= 0x2030000:
    # work around distutils complaints under Python 2.2.x
    extraArguments = {
        'classifiers': [
            """License :: OSI Approved :: BSD License""",
            """Programming Language :: Python""",
            """Topic :: Software Development :: Libraries :: Python Modules""",
            """Intended Audience :: Developers""",
        ],
        #'download_url': "http://sourceforge.net/projects/pydispatcher/files/pydispatcher/",
        'keywords': 'dispatcher,dispatch,pydispatch,event,signal,sender,receiver,propagate,multi-consumer,multi-producer,saferef,robustapply,apply',
        'long_description' : """Dispatcher mechanism for creating event models

PyDispatcher is an enhanced version of Patrick K. O'Brien's
original dispatcher.py module.  It provides the Python
programmer with a robust mechanism for event routing within
various application contexts.

Included in the package are the robustapply and saferef
modules, which provide the ability to selectively apply
arguments to callable objects and to reference instance
methods using weak-references.
""",
        'platforms': ['Any'],
    }
else:
    extraArguments = {
    }


version = [
    (line.split('=')[1]).strip().strip('"').strip("'")
    for line in open(os.path.join('pydispatch','__init__.py'))
    if line.startswith( '__version__' )
][0]

if __name__ == "__main__":
    ### Now the actual set up call
    setup (
        name = "PyDispatcher",
        version = version,
        description= "Multi-producer-multi-consumer signal dispatching mechanism",
        author = "Patrick K. O'Brien",
        author_email = "pydispatcher-devel@lists.sourceforge.net",
        url = "http://pydispatcher.sourceforge.net",
        license = "BSD-style, see license.txt for details",

        package_dir = {
            'pydispatch':'pydispatch',
        },

        packages = [
            'pydispatch',
        ],

        options = {
            'sdist':{'use_defaults':0, 'force_manifest':1},
            "install_lib":{"compile":0, "optimize":0},
            'bdist_rpm':{
                'group':'Libraries/Python',
                'provides':'python-dispatcher',
                'requires':"python",
            },
        },

        # registration metadata
        **extraArguments
    )

