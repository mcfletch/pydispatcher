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

    def testSharedSenderManyReceivers(self):
        """Many distinct receivers on one shared sender each fire exactly once.

        Exercises the O(1) presence-index fast path in connect(): wiring N
        receivers to a single sender must stay correct (no dropped or duplicated
        receivers) and leave the index consistent with the receiver lists.
        """
        sender = Dummy()
        signal = 'shared'
        hits = {}

        class R(object):
            def __init__(self, i):
                self.i = i
            def on(self, **named):
                hits[self.i] = hits.get(self.i, 0) + 1

        receivers = [R(i) for i in range(500)]
        for r in receivers:
            connect(r.on, signal, sender)
        # Re-connecting the same bound methods must dedup, not duplicate.
        for r in receivers:
            connect(r.on, signal, sender)
        send(signal, sender)
        assert all(hits.get(i) == 1 for i in range(500)), hits
        assert len(getReceivers(sender, signal)) == 500
        # The presence index mirrors the receiver list exactly.
        idx = dispatcher._receiverIndex[id(sender)][signal]
        assert len(idx) == 500, len(idx)
        # Disconnecting a subset stops only those, and prunes the index with it.
        for r in receivers[:200]:
            disconnect(r.on, signal, sender)
        hits.clear()
        send(signal, sender)
        assert sum(hits.values()) == 300, sum(hits.values())
        assert len(dispatcher._receiverIndex[id(sender)][signal]) == 300
        for r in receivers[200:]:
            disconnect(r.on, signal, sender)
        del receivers
        # Everything unwired: connections, back-refs, and the index are empty.
        assert id(sender) not in dispatcher._receiverIndex, dispatcher._receiverIndex
        self._isclean()


def getSuite():
    return unittest.makeSuite(DispatcherTests,'test')
        
if __name__ == "__main__":
    unittest.main ()
