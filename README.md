# PyDispatcher Multi-producer Multi-consumer Observables

PyDispatcher provides the Python programmer with a multiple-producer-multiple-consumer signal-registration and
routing infrastructure for use in multiple contexts. The mechanism
of PyDispatcher started life as a highly rated [recipe](http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/87056)
in the [Python Cookbook](http://aspn.activestate.com/ASPN/Python/Cookbook/). The [project](https://github.com/mcfletch/pydispatcher) aims
to include various enhancements to the recipe developed during use in
various applications. It is primarily maintained by [Mike Fletcher](http://www.vrplumber.com). A derivative
of the project provides the Django web framework's "signal" system.

## Installation

PyDispatcher is available on PyPI via standard PIP:
```
pip install PyDispatcher
```
[![Latest PyPI Version](https://img.shields.io/pypi/v/pydispatcher.svg)](https://pypi.python.org/pypi/pydispatcher)
[![Latest PyPI Version](https://img.shields.io/pypi/dm/pydispatcher.svg)](https://pypi.python.org/pypi/pydispatcher)


## Usage

[Documentation](https://mcfletch.github.io/pydispatcher/) is available
for detailed usage, but the basic idea is:

```
from pydispatch import dispatcher

metaKey = "moo"
MyNode = object()
event = {"sample": "event"}


def callback(event=None):
    """Handle signal being sent"""
    print("Signal received", event)


dispatcher.connect(callback, sender=MyNode, signal=metaKey)
dispatcher.send(metaKey, MyNode, event=event)
```


## Scaling

Two structures keep dispatch cost proportional to the work a signal actually
implies rather than to the size of the program around it.

**Wiring many receivers to one sender.** `connect()` guards against registering
the same receiver twice for a `(sender, signal)` pair. An index of what is
already registered answers that in constant time, so wiring N receivers to a
shared sender costs O(N) rather than O(N²). The index is an optimisation hint:
every real registration records itself there, so "not registered" is always
trustworthy, and a stale "registered" costs one scan and nothing else.

**Calling a receiver.** `robustApply` passes a receiver only the arguments it
will accept, which means knowing its parameters. Those come from the receiver's
code object, which never changes, so they are derived once and reused --
`robustapply.SIGNATURE_CACHE_SIZE` bounds how many are remembered. A call with
no keyword arguments needs no signature at all, since there is nothing to
subset.
