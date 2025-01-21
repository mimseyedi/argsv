"""

"""


from argsv.validators import (
    multival,
    typeval,
    fromto,
    eq,
    ne,
    gt,
)


VALID_PATTERN_ARG_TYPES = (
        {
            "param1": fromto(2, 3),
        },
        {
            "param1": typeval(int),
            "param2": lambda x: x > 5,
        },
        {
            "param1": multival(
                lambda x: x != 0,
                gt(5),
            ),
        },
)

INVALID_PATTERN_ARG_TYPES = (
    123,
    "string",
    [1, 2, 3],
    (1, 2),
    {1, 2, 3},
    None,
    3.14,
    True,
)

VALID_PATTERN_KEYS = (
    "param1",
    "string",
    'c',
    "p_",
    "1",
    "32.45",
    "123a",
    "!@#%^$",
)

INVALID_PATTERN_KEYS = (
    123,
    -1,
    2.5,
    True,
    (1, 2),
    ...,
    lambda x: x + 1,
    None,
)

VALID_PATTERN_VALUES = (
    lambda x: x > 5,
    typeval(float),
    fromto(1, 5, key=len),
    eq(10),
    multival(gt(5), ne(10)),
    len,
)

INVALID_PATTERN_VALUES = (
    2,
    3.5,
    True,
    None,
    "validator",
    'c',
    (1, 2,),
    [None, '2',],
    {1, 2, 3,},
)

VALID_PATTERN_MATCHES = (
    (
        lambda a=None, b=None: ..., {'a': eq(5), 'b': gt(0)}
    ),
    (
        lambda c=None: ..., {'c': typeval(int)}
    ),
    (
        lambda x=None, y=None, z=None: ..., {'z': fromto(1, 5)}
    ),
)

INVALID_PATTERN_MATCHES = (
    (
        lambda a=None, b=None: ..., {'g': eq(5), 'param': gt(0)}
    ),
    (
        lambda c=None: ..., {'...': typeval(int)}
    ),
    (
        lambda x=None, y=None, z=None: ..., {'p': fromto(1, 5)}
    ),
)

