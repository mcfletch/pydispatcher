from pydispatch.robustapply import *

import unittest
def noArgument():
    pass
def oneArgument (blah):
    pass
def twoArgument(blah, other):
    pass
class TestCases( unittest.TestCase ):
    def test01( self ):
        robustApply(noArgument )
    def test02( self ):
        self.assertRaises( TypeError, robustApply, noArgument, "this" )
    def test03( self ):
        self.assertRaises( TypeError, robustApply, oneArgument )
    def test04( self ):
        """Raise error on duplication of a particular argument"""
        self.assertRaises( TypeError, robustApply, oneArgument, "this", blah = "that" )
    def testPartials( self ):
        func0 = functools.partial(noArgument)
        robustApply(func0)

        func1 = functools.partial(oneArgument, blah = 10)
        robustApply(func1)

        func2 = functools.partial(twoArgument, other = 10)
        robustApply(func2, "first")

def getSuite():
    return unittest.makeSuite(TestCases,'test')


if __name__ == "__main__":
    unittest.main()
    