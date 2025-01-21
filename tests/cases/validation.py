"""

"""


from argsv import argsval
from argsv.validators import (
    eq,
    ne,
    gt,
    fromto,
    typeval,
    callval,
    iterval,
    multival,
)


@argsval(a=typeval(int))
def func1(a):
    return a


@argsval(a=typeval(int), b=typeval(float))
def func2(a, b):
    return a, b


@argsval(a=typeval(int), args=eq(3, key=len))
def func3(a, *args):
    return a, args


@argsval(args=iterval(typeval(int)))
def func4(*args):
    return args


@argsval(args=eq("Hello", key="__getitem__", args=(0,)))
def func5(*args):
    return args


@argsval(b=lambda x: x > 0)
def func6(a, b):
    return a, b


@argsval(a=fromto(1, 5), c=callval(lambda x: x > 5, OSError))
def func7(a, b, c):
    return a, b, c


@argsval(a=multival(typeval(int), lambda x: x > 0, ne(5)))
def func8(a):
    return a


@argsval(a=iterval(gt(0)))
def func9(a):
    return a


@argsval(a=iterval(iterval(typeval(int)), key='items'))
def func10(a):
    return a


@argsval(
    a=iterval(
        multival(
            typeval(str, key='__getitem__', args=(0,)),
            typeval(int, key='__getitem__', args=(1,)),
        ), key='items'
    )
)
def func11(a):
    return a


SUCCESSFUL_VALIDATIONS = (
    (func1, 2),
    (func2, 5, 3.2),
    (func3, 1, "first", "second", "third"),
    (func4, 2, 5, 10, 2),
    (func5, "Hello", "OPS!"),
    (func6, 9, 1),
    (func7, 3, 100000, 6),
    (func8, 3),
    (func9, [1, 2, 3, 4, 5, 6]),
    (func10, {1: 0, 2: 4}),
    (func11, {"a": 0, "b": 4}),
)

FAILED_VALIDATIONS = (
    (func1, "hello"),
    (func2, 5, 3),
    (func3, 1, "first", "second", "third", "OPS"),
    (func4, 2, 5, "123", 1.3),
    (func5, "bye", "OPS!", "zzZZzz"),
    (func6, 9, -1),
    (func7, 2, -99, 5),
    (func8, 5),
    (func8, 0),
    (func8, "OPS!"),
    (func9, [1, 2, 3, 0, 5, 6]),
    (func10, {1: 0, 2.2: 4}),
    (func11, {"a": 0, 1: 4}),
)