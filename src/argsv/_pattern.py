"""
@rgs✔

This file is about Patterns.
Patterns are templates that can be used to specify,
in the form of a dictionary or kwargs,
how each argument should be validated.
Pattern keys must be the names of parameters of
a callable and their values must be a callable or validator.

The Pattern class is implemented so that patterns
are specific objects that can be worked with in
a more convenient and controlled way.
"""


# Postponed annotations: enable
from __future__ import annotations
# Standard imports
from inspect import getcallargs
from typing import (
    Any,
    Dict,
    Union,
    Iterator,
    Callable,
)
# Internal imports
from ._validators import (
    Validator,
    CallVal,
)
from .errors import PatternError


# Defining a type for Pattern for easier access
PatternType = Dict[
    str,
    Union[Validator, Callable[[Any], None]]
]


class Pattern:
    """
    The Pattern class is responsible for creating Pattern objects.
    Objects that can bind validation patterns to arguments
    by referring to parameter names to make the
    validation process more specific and orderly.
    Pattern objects are created by default in the 'ArgsVal'
    class for validating arguments.

    Pattern structure::

        dict   --> {"parameter_name": Validator | Callable}
        kwargs --> parameter_name = Validator | Callable

    Pattern objects have a method called 'match' that
    checks their match with a callable.

    Also, using a method called 'get_validator', you can
    get the validator by referring to the name of the
    parameter to which the argument is sent.
    """

    def __init__(
        self,
        pattern: PatternType,
    ) -> None:
        self._pattern = self._pattern_validation(pattern)

    @property
    def pattern(self) -> PatternType:
        return self._pattern

    def get_validator(self, arg: str) -> Validator:
        """
        This method can return the corresponding Validator
        by receiving the name of the parameter that
        was passed as an argument.

        :param arg: Argument name
        :return: Validator
        """

        # Get argument validator
        v = self._pattern.get(arg)
        # If there is no validator for the argument
        if v is None:
            raise PatternError(
                f"There is no validator "
                f"for this argument: '{arg}'"
            )
        return v

    def __iter__(self) -> Iterator:
        return iter(self._pattern.items())

    @staticmethod
    def _pattern_validation(
        pattern: PatternType,
    ) -> PatternType:
        """
        This method is responsible for validating the received
        Pattern in the form of a dictionary and, if approved,
        returning the same dictionary.

        :param pattern: Pattern in dictionary format
        :return: PatternType
        """

        # Is Pattern a dict?
        if not isinstance(pattern, dict):
            err_msg = (
                f"Patterns must be defined "
                f"in the form of a 'dict'"
            )
            raise PatternError(err_msg)
        # Iterate through Pattern items
        for a, v in pattern.items():
            # Are Pattern keys of type string?
            if not isinstance(a, str):
                err_msg = (
                    f"All Pattern keys must "
                    f"be of type 'str'. "
                    f"Received: {a} from {type(a)}"
                )
                raise PatternError(err_msg)
            # Are Pattern values Callable or Validator?
            if callable(v):
                if not isinstance(v, Validator):
                    # If it was a callable
                    # it becomes a callable Validator.
                    pattern[a] = CallVal(v)
                    continue
            else:
                # Throw an exception
                # if none of these conditions apply.
                err_msg = (
                    "All Pattern values must "
                    "be of type 'Validator'. "
                    f"Received: {v} from {type(v)}"
                )
                raise PatternError(err_msg)
        # Return the dict itself, if confirmed
        return pattern

    def match(
        self,
        callable_: Callable,
        *args,
        **kwargs,
    ) -> Pattern:
        """
        This method compares the Pattern object with a callable
        along with its arguments and, if there is a match,
        returns the Pattern object for verification.

        :param callable_: A callable object
        :param args: Any
        :param kwargs: Any
        :return: Pattern
        """

        # Attaching arguments to their names
        args = getcallargs(
            callable_,
            *args,
            **kwargs
        )
        # Iterating in Pattern
        for param, _ in self:
            # Checking for Pattern keys in argument names
            if param not in args.keys():
                err_msg = (
                    "Pattern does not match callable. "
                    f"There is no parameter "
                    f"named '{param}' in callable"
                )
                raise PatternError(err_msg)
        # Returning the Pattern itself
        return self

    def __repr__(self):
        return f"ValidationPattern({self._pattern})"