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
        try:
            from importlib import metadata
        except ImportError:
            pass
        else:
            version = metadata.version("pydispatcher")
            version = [int(x) for x in version.split('.')]
            assert version >= [2,0,7], "Our installed version did not pick up configured attribute pydispatch.__version__"
