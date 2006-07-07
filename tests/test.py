import unittest
from pydispatch.tests import test_dispatcher,test_robustapply, test_saferef

def getSuite():
	set = []
	for module in [
		test_dispatcher,
		test_robustapply,
		test_saferef,
	]:
		set.append( module.getSuite() )
	return unittest.TestSuite(
		set
	)

if __name__ == "__main__":
	unittest.main(defaultTest="getSuite")
