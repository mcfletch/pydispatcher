from pydispatch.dispatcher import *
from pydispatch import dispatcher, robust

import unittest
def x(a):
    return a

class Dummy( object ):
    pass
class Callable(object):
    def __call__( self, a ):
        return a
    def a( self, a ):
        return a

class Callable2(object):
    def a(self, val):
        disconnect(self.a, "test")
        return val

class DispatcherTests(unittest.TestCase):
    """Test suite for dispatcher (barely started)"""

    def _isclean( self ):
        """Assert that everything has been cleaned up automatically"""
        assert len(dispatcher.sendersBack) == 0, dispatcher.sendersBack
        assert len(dispatcher.connections) == 0, dispatcher.connections
        assert len(dispatcher.senders) == 0, dispatcher.senders
    
    def testExact (self):
        a = Dummy()
        signal = 'this'
        connect( x, signal, a )
        expected = [(x,a)]
        result = send('this',a, a=a)
        assert result == expected,"""Send didn't return expected result:\n\texpected:%s\n\tgot:%s"""% (expected, result)
        disconnect( x, signal, a )
        assert len(list(getAllReceivers(a,signal))) == 0
        self._isclean()
    def testAnonymousSend(self):
        a = Dummy()
        signal = 'this'
        connect( x, signal )
        expected = [(x,a)]
        result = send(signal,None, a=a)
        assert result == expected,"""Send didn't return expected result:\n\texpected:%s\n\tgot:%s"""% (expected, result)
        disconnect( x, signal )
        assert len(list(getAllReceivers(None,signal))) == 0
        self._isclean()
    def testAnyRegistration(self):
        a = Dummy()
        signal = 'this'
        connect( x, signal, Any )
        expected = [(x,a)]
        result = send('this',object(), a=a)
        assert result == expected,"""Send didn't return expected result:\n\texpected:%s\n\tgot:%s"""% (expected, result)
        disconnect( x, signal, Any )
        expected = []
        result = send('this',object(), a=a)
        assert result == expected,"""Send didn't return expected result:\n\texpected:%s\n\tgot:%s"""% (expected, result)
        assert len(list(getAllReceivers(Any,signal))) == 0

        self._isclean()
        
    def testAnyRegistration2(self):
        a = Dummy()
        signal = 'this'
        connect( x, Any, a )
        expected = [(x,a)]
        result = send(signal,a, a=a)
        assert result == expected,"""Send didn't return expected result:\n\texpected:%s\n\tgot:%s"""% (expected, result)
        disconnect( x, Any, a )
        assert len(list(getAllReceivers(a,Any))) == 0
        self._isclean()
    def testGarbageCollected(self):
        a = Callable()
        b = Dummy()
        signal = 'this'
        connect( a.a, signal, b )
        expected = []
        del a
        result = send('this',b, a=b)
        assert result == expected,"""Send didn't return expected result:\n\texpected:%s\n\tgot:%s"""% (expected, result)
        assert len(list(getAllReceivers(b,signal))) == 0, """Remaining handlers: %s"""%(getAllReceivers(b,signal),)
        self._isclean()
    def testGarbageCollectedObj(self):
        class x:
            def __call__( self, a ):
                return a
        a = Callable()
        b = Dummy()
        signal = 'this'
        connect( a, signal, b )
        expected = []
        del a
        result = send('this',b, a=b)
        assert result == expected,"""Send didn't return expected result:\n\texpected:%s\n\tgot:%s"""% (expected, result)
        assert len(list(getAllReceivers(b,signal))) == 0, """Remaining handlers: %s"""%(getAllReceivers(b,signal),)
        self._isclean()


    def testMultipleRegistration(self):
        a = Callable()
        b = Dummy()
        signal = 'this'
        connect( a, signal, b )
        connect( a, signal, b )
        connect( a, signal, b )
        connect( a, signal, b )
        connect( a, signal, b )
        connect( a, signal, b )
        result = send('this',b, a=b)
        assert len( result ) == 1, result
        assert len(list(getAllReceivers(b,signal))) == 1, """Remaining handlers: %s"""%(getAllReceivers(b,signal),)
        del a
        del b
        del result
        self._isclean()
    def testRobust( self ):
        """Test the sendRobust function"""
        signal = 'this'
        def fails( ):
            raise ValueError( signal )
        a = object()
        connect( fails, Any, a )
        result = robust.sendRobust(signal,a, a=a)
        err = result[0][1]
        assert isinstance( err, ValueError )
        assert err.args == (signal,)
    def testParameterRepr(self):
        assert repr(dispatcher.Any) == '_Any', repr(dispatcher.Any)
        assert str(dispatcher.Any) == '_Any', str(dispatcher.Any)
    def testNoNoneSignal(self):
        self.assertRaises(
            errors.DispatcherTypeError, 
            dispatcher.connect,  x, signal=None
        )
        self.assertRaises(
            errors.DispatcherTypeError, 
            dispatcher.disconnect,  x, signal=None
        )
    def testDisconnectUnconnected(self):
        self.assertRaises(
            errors.DispatcherKeyError, 
            dispatcher.disconnect,  x, signal='not-registered'
        )
    def testDisconnectDuringCall(self):
        val0 = Callable2()
        connect(val0.a, "test")
        val1 = Callable2()
        connect(val1.a, "test")

        # Then we should have two connections.
        assert len(list(getAllReceivers(signal = "test"))) == 2

        # When sending the signal
        result = send("test", val = 10)

        # Then we should get two results
        assert result == [(val0.a, 10), (val1.a, 10)]
        # And both connections should be removed
        assert len(list(getAllReceivers(signal = "test"))) == 0


def getSuite():
    return unittest.makeSuite(DispatcherTests,'test')
        
if __name__ == "__main__":
    unittest.main ()
