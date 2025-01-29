"""
@rgs✔

This file is about the Validators that are implemented as
built-in in argsv to provide convenient and fast interfaces
for common argument validations.

This file contains functions that return a Validator.
These functions can be used to validate
arguments and even combine them.

These Validators are actually interfaces between
the programmer and the Validator classes implemented
in `argsv._validators`.

In this way, they are available and can
be used for greater convenience.
"""


# Standard imports
from typing import (
    Any,
    Dict,
    Type,
    Union,
    Tuple,
    Optional,
    Container,
)
# Internal imports
import argsv._validators as v


def callval(
    callable_: v.CallableType,
    exc: Optional[Type[BaseException]]=None,
    exc_msg: Optional[str]=None,
    *,
    key: v.KeyType=None,
    args: Optional[Tuple[Any, ...]]=None,
    kwargs: Optional[Dict[str, Any]]=None,
    aloc: Optional[int]=None,
) -> v.Validator:
    """
    This is a validator for validating the arguments
    of a callable that performs the validation process
    on the callable it receives.

    The received callable that is responsible for validating
    can only have one parameter (the parameter that must receive
    the argument to be validated).

    This callable validator can also handle the validation
    and generate errors internally by returning None
    or delegate this responsibility to **'callval'** by returning
    values that can be interpreted as **bool**.
    In this case, if the return result of the callable validator
    is **False**, the **'callval'** itself generates the specified error.

    Example usage::

        from argsv import argsval
        @argsval(a=callval(lambda x: x > 0))
        def dummy(a):
            return a

    You can specify the exception type with **'exc'** and also the message
    that should be published when an error occurs in **'exc_msg'**.

    You can validate an attribute or function with the desired
    argument by setting the **'key'** value, instead of
    directly validating the argument.

    Example usage::

        from argsv import argsval
        @argsval(a=lambda x: x == 3, key=len)
        def dummy(a):
            return a

    Here, instead of validating the original value of the argument,
    the output of the len function is validated against the input
    of the argument and finally it is checked whether
    the length of `a` is `equal to 3 or not`.

    If the validation key is a callable,
    its positional and keyword arguments can be passed
    to it via **'args'** and **'kwargs'**.

    If you are using a function as a Validation Key
    that does not take the argument being validated
    as the first input, you can specify the location
    where the argument should be sent with the **'aloc'** parameter.

    :param callable_: A CallableType object
    :param exc: Exception type
    :param exc_msg: Exception message
    :param key: Validation key (callable | attribute)
    :param args: Validation key args
    :param kwargs: Validation key kwargs
    :param aloc: The location of arg in Validation key
    :return: Validator
    """

    return v.CallVal(
        callable_,
        exc,
        exc_msg,
        key=key,
        args=args,
        kwargs=kwargs,
        aloc=aloc,
    )


def multival(
    *validators: Union[v.Validator, v.CallableType],
) -> v.Validator:
    """
    This is a validator for validating the arguments
    of a callable, which can host other validators to perform
    multiple validations on a single argument.

    The values passed to **'multival'** must either
    be a **validator** or a **callable** that accepts an argument.

    Example usage::

        from argsv import argsval
        @argsval(
            a=multival(
                lambda x: x > 5,
                lambda x: x != 7,
            )
        )
        def dummy(a):
            return a

    Here, with two conditions or lambda validators, using **'multival'**,
    the argument passed to the parameter `a` is validated.
    According to the conditions specified by the validators, the argument
    `a` must be greater than **5** but must not be equal to **7**.

    :param validators: *(Validator | CallableType)
    :return: Validator
    """

    return v.MultiVal(*validators)


def iterval(
    validator: Union[v.Validator, v.CallableType],
    exc: Optional[Type[BaseException]]=None,
    exc_msg: Optional[str]=None,
    *,
    key: v.KeyType=None,
    args: Optional[Tuple[Any, ...]]=None,
    kwargs: Optional[Dict[str, Any]]=None,
    aloc: Optional[int]=None,
) -> v.Validator:
    """
    This validator is used to validate arguments
    that are **iterable** and the validation operation is to
    be performed on their items.

    In fact, this validator, upon receiving a **validator**
    and an argument of type **iterable**, moves through the received
    iterable and validates the iterable items specified by the validator.

    Example usage::

        from argsv import argsval
        @argsval(a=iterval(lambda x: x > 0))
        def dummy(a: Iterable):
            return a

    In this example, **'iterval'** checks whether all items in the
    iterable argument passed to `a` are greater than zero
    and are considered positive numbers.

    You can specify the exception type with **'exc'** and also the message
    that should be published when an error occurs in **'exc_msg'**.

    You can validate an attribute or function with the desired
    argument by setting the **'key'** value, instead of
    directly validating the argument.

    Example usage::

        from argsv import argsval
        @argsval(
            a=iterval(
                lambda x: x > 10,
                key=lambda x: x ** 2,
            )
        )
        def dummy(a: Iterable)
            return a

    In this example, instead of validating the
    original values of `a`, the **squares** of the items of
    `a` are validated and are accepted if they are all `greater than 10`.

    If the validation key is a callable,
    its positional and keyword arguments can be passed
    to it via **'args'** and **'kwargs'**.

    If you are using a function as a Validation Key
    that does not take the argument being validated
    as the first input, you can specify the location
    where the argument should be sent with the **'aloc'** parameter.

    :param validator: A (Validator | CallableType) object
    :param exc: Exception type
    :param exc_msg: Exception message
    :param key: Validation key (callable | attribute)
    :param args: Validation key args
    :param kwargs: Validation key kwargs
    :param aloc: The location of arg in Validation key
    :return: Validator
    """

    return v.IterVal(
        validator,
        exc,
        exc_msg,
        key=key,
        args=args,
        kwargs=kwargs,
        aloc=aloc,
    )


def typeval(
    type_: Union[type, Tuple[type, ...]],
    exc: Optional[Type[BaseException]]=None,
    exc_msg: Optional[str]=None,
    *,
    key: v.KeyType=None,
    args: Optional[Tuple[Any, ...]]=None,
    kwargs: Optional[Dict[str, Any]]=None,
    aloc: Optional[int]=None,
) -> v.Validator:
    """
    This validator can validate the type of an argument.
    Using **'typeval'**, just like the built-in **isinstance** function,
    it is possible to check and validate the type of
    an argument and the received type must be
    a specific **type**, a **tuple of types**, or a **Union**.

    Example usage::

        from argsv import argsval
        @argsval(a=typeval(float))
        def dummy(a):
            return a

    You can specify the exception type with **'exc'** and also the message
    that should be published when an error occurs in **'exc_msg'**.

    You can validate an attribute or function with the desired
    argument by setting the **'key'** value, instead of
    directly validating the argument.

    Example usage::

        from argsv import argsval
        @argsval(a=typeval(Iterator, key="__iter__"))
        def dummy(a):
            return a

    Here, it is checked whether the return value from the
    **'__iter__()'** dunder-method, the argument passed to the
    `a` parameter, is of type **Iterator** or not.

    If the validation key is a callable,
    its positional and keyword arguments can be passed
    to it via **'args'** and **'kwargs'**.

    If you are using a function as a Validation Key
    that does not take the argument being validated
    as the first input, you can specify the location
    where the argument should be sent with the **'aloc'** parameter.

    :param type_: specific type, a tuple of types, or a Union
    :param exc: Exception type
    :param exc_msg: Exception message
    :param key: Validation key (callable | attribute)
    :param args: Validation key args
    :param kwargs: Validation key kwargs
    :param aloc: The location of arg in Validation key
    :return: Validator
    """

    return v.TypeVal(
        type_,
        exc,
        exc_msg,
        key=key,
        args=args,
        kwargs=kwargs,
        aloc=aloc,
    )


def fromto(
    from_: int,
    to_: int,
    exc: Optional[Type[BaseException]]=None,
    exc_msg: Optional[str]=None,
    *,
    key: v.KeyType=None,
    args: Optional[Tuple[Any, ...]]=None,
    kwargs: Optional[Dict[str, Any]]=None,
    aloc: Optional[int]=None,
) -> v.Validator:
    """
    This validator is used to validate arguments
    that are supposed to be in a specific range of numbers.

    **'fromto'**, by receiving a start point and an end point,
    generates a specified range and validates an
    argument within this range.

    Note that the start and end points must be of
    type number (**<'int'>**, **<'float'>**).

    Example usage::

        from argsv import argsval
        @argsval(a=fromto(1, 5))
        def dummy(a):
            return a

    In this example, it checks whether `a`
    is between **1** and **5** or not?

    `Note` that **1** and **5** are also considered part of the range!

    You can specify the exception type with **'exc'** and also the message
    that should be published when an error occurs in **'exc_msg'**.

    You can validate an attribute or function with the desired
    argument by setting the **'key'** value, instead of
    directly validating the argument.

    Example usage::

        from argsv import argsval
        @argsval(a=fromto(1, 3), key=len)
        def dummy(a: list):
            return a

    Here we check whether the **length** of 'a' is
    between **1** and **3** or not.

    If the validation key is a callable,
    its positional and keyword arguments can be passed
    to it via **'args'** and **'kwargs'**.

    If you are using a function as a Validation Key
    that does not take the argument being validated
    as the first input, you can specify the location
    where the argument should be sent with the **'aloc'** parameter.

    :param from_: start point
    :param to_: end point
    :param exc: Exception type
    :param exc_msg: Exception message
    :param key: Validation key (callable | attribute)
    :param args: Validation key args
    :param kwargs: Validation key kwargs
    :param aloc: The location of arg in Validation key
    :return: Validator
    """

    return v.FromTo(
        from_,
        to_,
        exc,
        exc_msg,
        key=key,
        args=args,
        kwargs=kwargs,
        aloc=aloc,
    )


def eq(
    other: Any,
    exc: Optional[Type[BaseException]]=None,
    exc_msg: Optional[str]=None,
    *,
    key: v.KeyType=None,
    args: Optional[Tuple[Any, ...]]=None,
    kwargs: Optional[Dict[str, Any]]=None,
    aloc: Optional[int]=None,
) -> v.Validator:
    """
    This validator is a comparison validator that compares an
    argument to another object, and specifically,
    this validator is responsible for **'equality'** validation.

    Example usage::

        from argsv import argsval
        @argsval(a=eq(5))
        def dummy(a):
            return a

    You can specify the exception type with **'exc'** and also the message
    that should be published when an error occurs in **'exc_msg'**.

    You can validate an attribute or function with the desired
    argument by setting the **'key'** value, instead of
    directly validating the argument.

    Example usage::

        from argsv import argsval
        @argsval(a=eq(3), key=len)
        def dummy(a: list):
            return a

    Here it is checked that the **length** of `a`
    must be equal to **3**.

    If the validation key is a callable,
    its positional and keyword arguments can be passed
    to it via **'args'** and **'kwargs'**.

    If you are using a function as a Validation Key
    that does not take the argument being validated
    as the first input, you can specify the location
    where the argument should be sent with the **'aloc'** parameter.

    :param other: The object to be compared with
    :param exc: Exception type
    :param exc_msg: Exception message
    :param key: Validation key (callable | attribute)
    :param args: Validation key args
    :param kwargs: Validation key kwargs
    :param aloc: The location of arg in Validation key
    :return: Validator
    """

    return v.CompVal(
        other,
        "==",
        exc,
        exc_msg,
        key=key,
        args=args,
        kwargs=kwargs,
        aloc=aloc,
    )


def ne(
    other: Any,
    exc: Optional[Type[BaseException]]=None,
    exc_msg: Optional[str]=None,
    *,
    key: v.KeyType=None,
    args: Optional[Tuple[Any, ...]]=None,
    kwargs: Optional[Dict[str, Any]]=None,
    aloc: Optional[int]=None,
) -> v.Validator:
    """
    This validator is a comparison validator that compares an
    argument to another object, and specifically,
    this validator is responsible for **'inequality'** validation.

    Example usage::

        from argsv import argsval
        @argsval(a=ne(3))
        def dummy(a):
            return a

    You can specify the exception type with **'exc'** and also the message
    that should be published when an error occurs in **'exc_msg'**.

    You can validate an attribute or function with the desired
    argument by setting the **'key'** value, instead of
    directly validating the argument.

    Example usage::

        from argsv import argsval
        @argsval(a=ne(0), key=len)
        def dummy(a: list):
            return a

    Here it is checked that the **length** of `a`
    should **not be equal** to **zero**.

    If the validation key is a callable,
    its positional and keyword arguments can be passed
    to it via **'args'** and **'kwargs'**.

    If you are using a function as a Validation Key
    that does not take the argument being validated
    as the first input, you can specify the location
    where the argument should be sent with the **'aloc'** parameter.

    :param other: The object to be compared with
    :param exc: Exception type
    :param exc_msg: Exception message
    :param key: Validation key (callable | attribute)
    :param args: Validation key args
    :param kwargs: Validation key kwargs
    :param aloc: The location of arg in Validation key
    :return: Validator
    """

    return v.CompVal(
        other,
        "!=",
        exc,
        exc_msg,
        key=key,
        args=args,
        kwargs=kwargs,
        aloc=aloc,
    )


def gt(
    other: Any,
    exc: Optional[Type[BaseException]]=None,
    exc_msg: Optional[str]=None,
    *,
    key: v.KeyType=None,
    args: Optional[Tuple[Any, ...]]=None,
    kwargs: Optional[Dict[str, Any]]=None,
    aloc: Optional[int]=None,
) -> v.Validator:
    """
    This validator is a comparison validator that compares an
    argument to another object, and specifically,
    this validator validates the argument to see
    if it is **'greater-than'** the received object.

    Example usage::

        from argsv import argsval
        @argsval(a=gt(0))
        def dummy(a):
            return a

    You can specify the exception type with **'exc'** and also the message
    that should be published when an error occurs in **'exc_msg'**.

    You can validate an attribute or function with the desired
    argument by setting the **'key'** value, instead of
    directly validating the argument.

    Example usage::

        from argsv import argsval
        @argsval(a=gt(0), key=len)
        def dummy(a: list):
            return a

    Here it is checked that the **length** of `a`
    must be **greater** than **zero**.

    If the validation key is a callable,
    its positional and keyword arguments can be passed
    to it via **'args'** and **'kwargs'**.

    If you are using a function as a Validation Key
    that does not take the argument being validated
    as the first input, you can specify the location
    where the argument should be sent with the **'aloc'** parameter.

    :param other: The object to be compared with
    :param exc: Exception type
    :param exc_msg: Exception message
    :param key: Validation key (callable | attribute)
    :param args: Validation key args
    :param kwargs: Validation key kwargs
    :param aloc: The location of arg in Validation key
    :return: Validator
    """

    return v.CompVal(
        other,
        ">",
        exc,
        exc_msg,
        key=key,
        args=args,
        kwargs=kwargs,
        aloc=aloc,
    )


def lt(
    other: Any,
    exc: Optional[Type[BaseException]]=None,
    exc_msg: Optional[str]=None,
    *,
    key: v.KeyType=None,
    args: Optional[Tuple[Any, ...]]=None,
    kwargs: Optional[Dict[str, Any]]=None,
    aloc: Optional[int]=None,
) -> v.Validator:
    """
    This validator is a comparison validator that compares an
    argument to another object, and specifically,
    this validator validates the argument to see
    if it is **'less-than'** the received object.

    Example usage::

        from argsv import argsval
        @argsval(a=lt(10))
        def dummy(a):
            return a

    You can specify the exception type with **'exc'** and also the message
    that should be published when an error occurs in **'exc_msg'**.

    You can validate an attribute or function with the desired
    argument by setting the **'key'** value, instead of
    directly validating the argument.

    Example usage::

        from argsv import argsval
        @argsval(a=lt(3), key=len)
        def dummy(a: list):
            return a

    Here it is checked that the **length** of `a`
    must be **less** than **3**.

    If the validation key is a callable,
    its positional and keyword arguments can be passed
    to it via **'args'** and **'kwargs'**.

    If you are using a function as a Validation Key
    that does not take the argument being validated
    as the first input, you can specify the location
    where the argument should be sent with the **'aloc'** parameter.

    :param other: The object to be compared with
    :param exc: Exception type
    :param exc_msg: Exception message
    :param key: Validation key (callable | attribute)
    :param args: Validation key args
    :param kwargs: Validation key kwargs
    :param aloc: The location of arg in Validation key
    :return: Validator
    """

    return v.CompVal(
        other,
        "<",
        exc,
        exc_msg,
        key=key,
        args=args,
        kwargs=kwargs,
        aloc=aloc,
    )


def ge(
    other: Any,
    exc: Optional[Type[BaseException]]=None,
    exc_msg: Optional[str]=None,
    *,
    key: v.KeyType=None,
    args: Optional[Tuple[Any, ...]]=None,
    kwargs: Optional[Dict[str, Any]]=None,
    aloc: Optional[int]=None,
) -> v.Validator:
    """
    This validator is a comparison validator that compares an
    argument to another object, and specifically,
    this validator validates the argument to see
    if it is **'greater-than-or-equal'** the received object.

    Example usage::

        from argsv import argsval
        @argsval(a=ge(0))
        def dummy(a):
            return a

    You can specify the exception type with **'exc'** and also the message
    that should be published when an error occurs in **'exc_msg'**.

    You can validate an attribute or function with the desired
    argument by setting the **'key'** value, instead of
    directly validating the argument.

    Example usage::

        from argsv import argsval
        @argsval(a=ge(1), key=len)
        def dummy(a: list):
            return a

    Here it is checked that the **length** of `a`
    must be **greater** than or **equal** to **1**.

    If the validation key is a callable,
    its positional and keyword arguments can be passed
    to it via **'args'** and **'kwargs'**.

    If you are using a function as a Validation Key
    that does not take the argument being validated
    as the first input, you can specify the location
    where the argument should be sent with the **'aloc'** parameter.

    :param other: The object to be compared with
    :param exc: Exception type
    :param exc_msg: Exception message
    :param key: Validation key (callable | attribute)
    :param args: Validation key args
    :param kwargs: Validation key kwargs
    :param aloc: The location of arg in Validation key
    :return: Validator
    """

    return v.CompVal(
        other,
        ">=",
        exc,
        exc_msg,
        key=key,
        args=args,
        kwargs=kwargs,
        aloc=aloc,
    )


def le(
    other: Any,
    exc: Optional[Type[BaseException]]=None,
    exc_msg: Optional[str]=None,
    *,
    key: v.KeyType=None,
    args: Optional[Tuple[Any, ...]]=None,
    kwargs: Optional[Dict[str, Any]]=None,
    aloc: Optional[int]=None,
) -> v.Validator:
    """
    This validator is a comparison validator that compares an
    argument to another object, and specifically,
    this validator validates the argument to see
    if it is **'less-than-or-equal'** the received object.

    Example usage::

        from argsv import argsval
        @argsval(a=le(9))
        def dummy(a):
            return a

    You can specify the exception type with **'exc'** and also the message
    that should be published when an error occurs in **'exc_msg'**.

    You can validate an attribute or function with the desired
    argument by setting the **'key'** value, instead of
    directly validating the argument.

    Example usage::

        from argsv import argsval
        @argsval(a=le(3), key=len)
        def dummy(a: list):
            return a

    Here it is checked that the **length** of `a`
    must be **less** than or **equal** to **3**.

    If the validation key is a callable,
    its positional and keyword arguments can be passed
    to it via **'args'** and **'kwargs'**.

    If you are using a function as a Validation Key
    that does not take the argument being validated
    as the first input, you can specify the location
    where the argument should be sent with the **'aloc'** parameter.

    :param other: The object to be compared with
    :param exc: Exception type
    :param exc_msg: Exception message
    :param key: Validation key (callable | attribute)
    :param args: Validation key args
    :param kwargs: Validation key kwargs
    :param aloc: The location of arg in Validation key
    :return: Validator
    """

    return v.CompVal(
        other,
        "<=",
        exc,
        exc_msg,
        key=key,
        args=args,
        kwargs=kwargs,
        aloc=aloc,
    )


def inval(
    container: Container,
    exc: Optional[Type[BaseException]]=None,
    exc_msg: Optional[str]=None,
    *,
    key: v.KeyType=None,
    args: Optional[Tuple[Any, ...]]=None,
    kwargs: Optional[Dict[str, Any]]=None,
    aloc: Optional[int]=None,
) -> v.Validator:
    """
    This validator validates the membership status of an
    argument in a container. When a container is taken,
    the callable argument must be present in it, otherwise the
    validation fails and an error is displayed.

    Example usage::

        from argsv import argsval
        @argsval(a=inval(range(1, 10)))
        def dummy(a):
            return a

    In this example, it checks whether `a` is a
    **single digit** number or not.

    You can specify the exception type with **'exc'** and also the message
    that should be published when an error occurs in **'exc_msg'**.

    You can validate an attribute or function with the desired
    argument by setting the **'key'** value, instead of
    directly validating the argument.

    Example usage::

        from argsv import argsval
        @argsval(a=inval(range(1, 4), key=len)
        def dummy(a: list):
            return a

    In this example, it checks whether the
    **length** of `a` is in the range **1** to **3**.

    If the validation key is a callable,
    its positional and keyword arguments can be passed
    to it via **'args'** and **'kwargs'**.

    If you are using a function as a Validation Key
    that does not take the argument being validated
    as the first input, you can specify the location
    where the argument should be sent with the **'aloc'** parameter.

    :param container: A container object
    :param exc: Exception type
    :param exc_msg: Exception message
    :param key: Validation key (callable | attribute)
    :param args: Validation key args
    :param kwargs: Validation key kwargs
    :param aloc: The location of arg in Validation key
    :return: Validator
    """

    return v.ContainsVal(
        container,
        False,
        exc,
        exc_msg,
        key=key,
        args=args,
        kwargs=kwargs,
        aloc=aloc,
    )


def notinval(
    container: Container,
    exc: Optional[Type[BaseException]]=None,
    exc_msg: Optional[str]=None,
    *,
    key: v.KeyType=None,
    args: Optional[Tuple[Any, ...]]=None,
    kwargs: Optional[Dict[str, Any]]=None,
    aloc: Optional[int]=None,
) -> v.Validator:
    """
    This validator validates the membership status
    of an argument in a container.
    When a container is taken, the callable argument must
    **not** be present in it, otherwise the
    validation will fail and an error will be displayed.

    Example usage::

        from argsv import argsval
        @argsval(a=notinval(range(1, 10)))
        def dummy(a):
            return a

    In this example, it checks whether `a` is a
    number with **more** than **one** digit.

    You can specify the exception type with **'exc'** and also the message
    that should be published when an error occurs in **'exc_msg'**.

    You can validate an attribute or function with the desired
    argument by setting the **'key'** value, instead of
    directly validating the argument.

    Example usage::

        from argsv import argsval
        @argsval(a=notinval(range(65, 123), key=ord))
        def dummy(a: str):
            return a

    In this example, with the help of validator **'notinval'** and
    validation key **'ord'**, it is checked whether the argument passed
    to the function is a member of the **alphabet** or not.

    If the validation key is a callable,
    its positional and keyword arguments can be passed
    to it via **'args'** and **'kwargs'**.

    If you are using a function as a Validation Key
    that does not take the argument being validated
    as the first input, you can specify the location
    where the argument should be sent with the **'aloc'** parameter.

    :param container: A container object
    :param exc: Exception type
    :param exc_msg: Exception message
    :param key: Validation key (callable | attribute)
    :param args: Validation key args
    :param kwargs: Validation key kwargs
    :param aloc: The location of arg in Validation key
    :return: Validator
    """

    return v.ContainsVal(
        container,
        True,
        exc,
        exc_msg,
        key=key,
        args=args,
        kwargs=kwargs,
        aloc=aloc,
    )