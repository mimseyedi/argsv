"""
@rgs✔

This file is the core and underlying part of the 'argsv' library.

Here, the ArgsVal class and the argsval decorator are implemented
to be the main tools for validating callable arguments.

Usage::

    @argsval(a=validator_a, b=validator_b)
        def add(a, b):
            return a + b
"""


from typing import(
    Any,
    Dict,
    Tuple,
    Callable,
)
from functools import wraps
from inspect import getcallargs

from ._pattern import (
    Pattern,
    PatternType,
)
from .errors import (
    ValidationError,
    ValidatorError,
)


class ArgsVal:
    """
    The ArgsVal class can specifically create objects that
    validate arguments passed to a callable object.
    This is done by passing a callable and its arguments
    along with a Pattern. The Pattern, which is a dictionary of
    callable parameter names with values of type Validator
    (Objects that are usually callable and can validate
    a specific argument by receiving a value.),
    specifies how the arguments passed to the callable parameters
    should be validated in order to be accepted!

    Example usage::

        def add(a, b):
            # Validation section
            pattern = {a: validator_a, b: validator_b}
            av = ArgsVal(function, pattern, a, b)
            av.validate()
            # Function code section
            return a + b

    :param callable_: A callable object whose arguments are to be validated.
    :param pattern: A Pattern, in the form of a dict (parameter name: Validator),
                    specifies how arguments should be validated.
    :param args: Positional arguments passed to callable.
    :param kwargs: Keyword arguments passed to callable.
    :return: ArgsVal object
    """

    def __init__(
        self,
        callable_: Callable,
        pattern: PatternType,
        *args: Tuple[Any, ...],
        **kwargs: Dict[str, Any],
    ) -> None:
        self._callable = self._check_callable(callable_)
        self._args = args
        self._kwargs = kwargs
        self._pattern = self._verify_pattern(pattern)

    @property
    def callable(self) -> Callable:
        return self._callable

    @property
    def pattern(self) -> Pattern:
        return self._pattern

    @property
    def args(self) -> Tuple[Any, ...]:
        return self._args

    @property
    def kwargs(self) -> Dict[str, Any]:
        return self._kwargs

    def validate(self) -> None:
        """
        This method is responsible for validating the callable arguments.
        This is done by referencing the Pattern and comparing
        the arguments to the conditions held by the Validator,
        and if validation fails, the exact information about the point
        where validation stopped will be displayed
        in the form of an exception.
        Otherwise, the callable will execute as it should.

        :return: None
        """
        # Attaching arguments to their parameter names
        args = getcallargs(
            self._callable,
            *self._args,
            **self._kwargs,
        )
        # Iterating inside the Pattern and calling Validators
        for name, v in self.pattern:
            # Store the argument in 'a'
            a = args.get(name)
            try:
                # Calling Validator with 'a'
                v(a)
            # Handling validator errors
            except ValidatorError:
                raise
            # Handling exceptions
            # and creating custom messages
            except BaseException as e:
                err_msg = (
                    "Validation stopped while checking "
                    f"the argument passed to parameter '{name}', "
                    f"in callable '{self._callable.__name__}'\n"
                    f"From validator: {v.name}\n"
                    f" └── {type(e).__name__}: {e}"
                )
                raise ValidationError(
                    err_msg
                ) from None

    def _verify_pattern(self, pattern: PatternType) -> Pattern:
        """
        Does Pattern match callable?
        This method determines whether the pattern matches the callable
        by calling the match method of a Pattern object.
        If yes, a Pattern object is returned, otherwise an exception is raised.

        :param pattern: A Pattern, in the form of a dict (parameter name: Validator),
                        specifies how arguments should be validated.
        :return: Pattern
        """

        return Pattern(
            pattern
        ).match(
            self._callable,
            *self._args,
            **self._kwargs,
        )

    @staticmethod
    def _check_callable(callable_: Callable) -> Callable:
        """
        This method validates the callable object and returns it if it passes.

        :param callable_: A callable object.
        :return: Callable
        """

        if not callable(callable_):
            err_msg = (
                f"'{type(callable_).__name__}' "
                "object is not callable"
            )
            raise TypeError(err_msg)
        return callable_

    def __repr__(self):
        return (
            f"ArgsVal(callable={self._callable}, "
            f"pattern={self._pattern}, "
            f"args={self._args},"
            f"kwargs={self.kwargs})"
        )

def argsval(**pattern) -> Callable:
    """
    The argsval function is a decorator for validating arguments
    passed to a callable. Using the ArgsVal class and a simple,
    easy-to-understand syntax, this decorator allows arguments to
    be validated outside the function body, so that functions
    can focus on what they need to do in their bodies.

    The argsval decorator safely and readably handles the validation
    of arguments outside the function body.

    Example usage::

        @argsval(a=validator_a, b=validator_b)
        def add(a, b):
            return a + b

    :param pattern: A Pattern, in the form of a dict (parameter name: Validator),
                    specifies how arguments should be validated.
    :return: Callable
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(
            *args: Tuple[Any, ...],
            **kwargs: Dict[str, Any],
        ) -> Any:
            ArgsVal(
                func, 
                pattern, 
                *args, 
                **kwargs,
            ).validate()
            return func(*args, **kwargs)
        return wrapper
    return decorator