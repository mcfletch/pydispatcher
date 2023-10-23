from pydispatch.robustapply import *
from pydispatch import robustapply

import unittest


class TestCases(unittest.TestCase):
    def test_keyword_only(self):
        """Test that we can handle a keyword-only argument via robustapply where there are *no* variadic args"""

        def foo(a, b, /, c, d, *, e):
            pass

        robustApply(foo, 1, 2, 3, 4, e=6)

    def test_keyword_only_after_args(self):
        """Test that we can handle a keyword-only argument via robustapply where there are *no* variadic args"""
        moos = []

        def foo(a, b, /, c, d, *m, e):
            moos.append(m)

        robustApply(foo, 1, 2, 3, 4, 8, e=6)
        assert moos == [(8,)], moos

    def test_positional_only(self):
        """Test that positional-only errors are properly raised"""

        def foo(a, b, /, c, d, *, e):
            pass

        self.assertRaises(TypeError, robustApply, foo, a=0, b=3, c=4, d=5, e=8)

    def test_prevent_passing_varargs(self):
        """Verify that passing varargs parameter name will not cause TypeError"""

        def foo(a, *moo, e):
            pass

        robustApply(foo, a=0, moo=(1, 2, 3), e=8)

    def test_prevent_passing_varnamed(self):
        """Verify that passing varnamed parameter name will not cause TypeError"""

        def foo(a, e, **moo):
            pass

        robustApply(foo, a=0, moo=(1, 2, 3), e=8)

    def test_argument_counts(self):
        """Sanity check for argcount with both varargs and named-only"""

        def foo(a, b, /, c, d, *m, e, **v):
            pass

        rec, co, startIndex = robustapply.function(foo)
        assert startIndex == 0, startIndex  # should be 0 for function
        assert rec is foo
        assert co
        assert co.co_argcount == 4, co.co_argcount
        assert co.co_varnames == ('a', 'b', 'c', 'd', 'e', 'm', 'v'), co.co_varnames
