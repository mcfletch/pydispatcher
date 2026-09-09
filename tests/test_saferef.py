from pydispatch.saferef import *

import unittest


class T1(object):
    def x(self):
        pass


def t2(obj):
    pass


class T2(object):
    def __call__(self, obj):
        pass


class Tester(unittest.TestCase):
    def setUp(self):
        ts = []
        ss = []
        for _x in range(5000):
            t = T1()
            ts.append(t)
            s = safeRef(t.x, self._closure)
            ss.append(s)
        ts.append(t2)
        ss.append(safeRef(t2, self._closure))
        for _x in range(30):
            t = T2()
            ts.append(t)
            s = safeRef(t, self._closure)
            ss.append(s)
        self.ts = ts
        self.ss = ss
        self.closureCount = 0

    def tearDown(self):
        del self.ts
        del self.ss

    def testIn(self):
        """Test the "in" operator for safe references (cmp)"""
        for t in self.ts[:50]:
            assert safeRef(t.x) in self.ss

    def testValid(self):
        """Test that the references are valid (return instance methods)"""
        for s in self.ss:
            assert s()

    def testShortCircuit(self):
        """Test that creation short-circuits to reuse existing references"""
        sd = {}
        for s in self.ss:
            sd[s] = 1
        for t in self.ts:
            if hasattr(t, 'x'):
                assert safeRef(t.x) in sd
            else:
                assert safeRef(t) in sd

    def testRepresentation(self):
        """Test that the reference object's representation works

        XXX Doesn't currently check the results, just that no error
            is raised
        """
        repr(self.ss[-1])

    def test(self):
        self.closureCount = 0
        wholeI = len(self.ts)
        for i in range(len(self.ts) - 1, -1, -1):
            del self.ts[i]
            if wholeI - i != self.closureCount:
                """Unexpected number of items closed, expected %s, got %s closed""" % (
                    wholeI - i,
                    self.closureCount,
                )

    def test_multipleRegistration(self):
        """GH#5 Test that doing multiple saferefs to the same object results in all callbacks being registered and called back"""
        for _iteration in range(5):
            callback, check = check_callback()
            test = T1()

            s = safeRef(test.x, self._closure)
            r = safeRef(test.x, callback)

            assert s is r
            assert callback in r.deletionMethods
            assert len(r.deletionMethods) == 2, r.deletionMethods

            del test

            assert len(check()) == 1, check()

    def _closure(self, ref):
        """Dumb utility mechanism to increment deletion counter"""
        self.closureCount += 1


def check_callback():
    """Construct a callback and was-called check

    This avoids the frame reference of the function from keeping
    objects alive during tests...
    """
    #
    counter = []

    def callback(*args, **named):
        counter.append((args, named))

    def check():
        return counter

    return callback, check


def getSuite():
    return unittest.makeSuite(Tester, 'test')


if __name__ == "__main__":
    unittest.main()
