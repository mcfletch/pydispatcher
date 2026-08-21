from pydispatch.robustapply import *
from pydispatch import robustapply

import unittest


def noArgument():
    pass


def oneArgument(blah):
    pass


def twoArgument(blah, other):
    pass


class TestCases(unittest.TestCase):
    def test01(self):
        robustApply(noArgument)

    def test02(self):
        self.assertRaises(TypeError, robustApply, noArgument, "this")

    def test03(self):
        self.assertRaises(TypeError, robustApply, oneArgument)

    def test04(self):
        """Raise error on duplication of a particular argument"""
        self.assertRaises(TypeError, robustApply, oneArgument, "this", blah="that")

    def test_signature_is_derived_once_per_code_object(self):
        """Everything robustApply needs about a receiver comes from its code
        object, which never changes: derive it once and reuse it."""
        robustapply._signature.cache_clear()
        for _ in range(5):
            robustApply(twoArgument, "this", other="that")
        info = robustapply._signature.cache_info()
        self.assertEqual(info.misses, 1)
        self.assertEqual(info.hits, 4)

    def test_a_call_with_no_keywords_needs_no_signature_at_all(self):
        """With nothing to subset, there is nothing to look up."""
        robustapply._signature.cache_clear()
        robustApply(twoArgument, "this", "that")
        info = robustapply._signature.cache_info()
        self.assertEqual((info.misses, info.hits), (0, 0))

    def test_distinct_signatures_are_not_confused(self):
        """Receivers are told apart by code object, not by name or arity."""
        robustapply._signature.cache_clear()
        seen = []

        def keyworded(alpha, **rest):
            seen.append(("keyworded", alpha, rest))

        def strict(alpha):
            seen.append(("strict", alpha))

        robustApply(keyworded, alpha=1, beta=2)
        robustApply(strict, alpha=1, beta=2)
        self.assertEqual(
            seen,
            [("keyworded", 1, {"beta": 2}), ("strict", 1)],
        )

    def test_bound_methods_drop_unacceptable_keywords(self):
        """A bound method's own first argument is not counted against it."""
        class Receiver(object):
            def __init__(self):
                self.calls = []

            def handler(self, signal=None):
                self.calls.append(signal)

        target = Receiver()
        robustApply(target.handler, signal="s", sender="unwanted")
        self.assertEqual(target.calls, ["s"])


def getSuite():
    return unittest.makeSuite(TestCases, 'test')


if __name__ == "__main__":
    unittest.main()
