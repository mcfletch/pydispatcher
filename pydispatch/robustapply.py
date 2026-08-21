"""Robust apply mechanism

Provides a function "call", which can sort out
what arguments a given callable object can take,
and subset the given arguments to match only
those which are acceptable.
"""
import sys
from functools import lru_cache
from types import FunctionType, MethodType

if sys.hexversion >= 0x3000000:
    im_func = '__func__'
    im_self = '__self__'
    im_code = '__code__'
    func_code = '__code__'
else:
    im_func = 'im_func'
    im_self = 'im_self'
    im_code = 'im_code'
    func_code = 'func_code'


def function(receiver):
    """Get function-like callable object for given receiver

    returns (function_or_method, codeObject, fromMethod)

    If fromMethod is true, then the callable already
    has its first argument bound
    """
    # The two shapes almost every receiver has, each settled by a single check
    # rather than by the attribute walk below. Neither is redirected by it: a
    # bound method's and a function's __call__ is a method-wrapper, carrying
    # neither im_func nor im_code, so this is the same answer arrived at sooner.
    if isinstance(receiver, MethodType):
        return receiver, receiver.__func__.__code__, 1
    if isinstance(receiver, FunctionType):
        return receiver, receiver.__code__, 0
    if hasattr(receiver, '__call__'):
        # Reassign receiver to the actual method that will be called.
        if hasattr(receiver.__call__, im_func) or hasattr(receiver.__call__, im_code):
            receiver = receiver.__call__
    if hasattr(receiver, im_func):
        # an instance-method...
        return receiver, getattr(getattr(receiver, im_func), func_code), 1
    elif not hasattr(receiver, func_code):
        raise ValueError('unknown reciever type %s %s' % (receiver, type(receiver)))
    return receiver, getattr(receiver, func_code), 0


VAR_ARGS = 4
VAR_NAMES = 8

# A code object is immutable, so what a receiver will accept never changes.
# Deriving it per call put a signature walk in front of every dispatch, which a
# scene with many receivers on one signal pays over and over. Bounded rather
# than unbounded because a process that compiles code at runtime would
# otherwise accumulate an entry per generated code object; the number of
# distinct receiver definitions in a program is far below this.
SIGNATURE_CACHE_SIZE = 4096


@lru_cache(maxsize=SIGNATURE_CACHE_SIZE)
def _signature(codeObject):
    """What robustApply needs to know about a receiver's parameters

    Returns ``(has_varnames, posonly_count, positional_names,
    posnamed_arguments, named_onlyarguments)``.

    ``co_varnames`` lists the parameters first -- positional-or-keyword
    (``co_argcount`` of them) then keyword-only (``co_kwonlyargcount``) --
    followed by any ``*args``/``**kwargs`` slot and then the function's ordinary
    local variables. The acceptable keyword names are exactly the keyword-only
    parameters; bounding by ``co_kwonlyargcount`` so a local that merely shares
    a caller's argument name (a receiver with an internal ``value``, say) is not
    mistaken for one.
    """
    argcount = codeObject.co_argcount
    posonly_count = getattr(codeObject, 'co_posonlyargcount', 0)
    kwonly_count = getattr(codeObject, 'co_kwonlyargcount', 0)
    return (
        bool(codeObject.co_flags & VAR_NAMES),
        posonly_count,
        codeObject.co_varnames[0:argcount],
        codeObject.co_varnames[posonly_count:argcount],
        codeObject.co_varnames[argcount : argcount + kwonly_count],
    )


def robustApply(receiver, *arguments, **named):
    """Call receiver with arguments and an appropriate subset of named

    The effect of this wrapper is to allow for specifying a large number
    of parameters which may not exist in the final function via named
    parameters, and have those parameters ignored in the final call.
    """
    receiver, codeObject, startIndex = function(receiver)
    if named:
        (
            has_varnames,
            posonly_count,
            positional_names,
            posnamed_arguments,
            named_onlyarguments,
        ) = _signature(codeObject)

        # Implements: You can't have a parameter in both args and keywords, reporting an easily debugged message
        # Implements: You can't have a posonly arg in named (as a side effect of the above)
        for name in positional_names[0 : len(arguments)]:
            if name in named:
                raise TypeError(
                    """Argument %r specified both positionally and as a keyword for calling %r"""
                    % (
                        name,
                        receiver,
                    )
                )
        # Implements: You can only passed keyword parameters if the parameter exists and is not a
        # positional-only parameter or a varargs or varkeywords paramter. Note that this silently
        # drops TypeErrors for passing the name of the varargs or varkeyword variables because it
        # only allows through the valid arg-names for the function
        if not has_varnames:
            acceptable = (
                posnamed_arguments[len(arguments) - posonly_count :] + named_onlyarguments
            )
            # fc does not have a **kwds type parameter, therefore
            # remove unacceptable arguments.
            named = {k: v for k, v in named.items() if k in acceptable}
    return receiver(*arguments, **named)
