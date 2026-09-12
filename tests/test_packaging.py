import os
import unittest

class PackagingTest(unittest.TestCase):
    def test_the_declarations_reach_a_consumer(self):
        """`py.typed` beside the modules is what tells a consumer's checker to
        read the declarations rather than answering `Any` for every call.

        This package sits under the rest of the observer mechanism, so without
        it `dispatcher.send`, `connect` and `robustapply` are unchecked in
        every package above -- and a wrong signal name or a wrong keyword there
        fails silently at run time, which is exactly what a checker catches.

        Installed rather than merely present in the checkout: the marker is a
        data file, and one that is not named in the packaging is one that never
        reaches the wheel.
        """
        import pydispatch
        marker = os.path.join(os.path.dirname(pydispatch.__file__), 'py.typed')
        assert os.path.exists(marker), marker

    def test_package_metadata(self):
        """The version a consumer reads is the one the module declares.

        `pydispatch.__version__` is the only place the number is written, and
        the packaging reads it from there. An install that answers with a
        different number is one whose metadata was built before the attribute
        moved -- which is what the `cache-keys` entry in `pyproject.toml`
        exists to prevent, and what a dependent resolving against PyPI instead
        of this checkout looks like from the inside.

        Compared as the strings they are, rather than as numbers: a version is
        `2.0.9a1` as readily as `2.0.9`, and a pre-release is not a lesser kind
        of release to a resolver.
        """
        from importlib import metadata
        import pydispatch
        installed = metadata.version('pydispatcher')
        assert installed == pydispatch.__version__, (
            'the installed metadata says %s and pydispatch.__version__ says %s'
            % (installed, pydispatch.__version__))
