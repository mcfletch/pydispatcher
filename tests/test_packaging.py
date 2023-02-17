import unittest 

class PackagingTest(unittest.TestCase):
    def test_package_metadata(self):
        try:
            from importlib import metadata 
        except ImportError:
            pass 
        else:
            version = metadata.version("pydispatcher")
            version = [int(x) for x in version.split('.')]
            assert version >= [2,0,7], "Our installed version did not pick up configured attribute pydispatch.__version__"
