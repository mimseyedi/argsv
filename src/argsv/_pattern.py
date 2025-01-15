"""

"""

from __future__ import annotations

from typing import (
    Any,
    Dict,
    Union,
    Iterator,
    Callable,
)
from inspect import getcallargs

from _validators import (
    Validator,
    CallableValidator,
)
from errors import PatternError


PatternType = Dict[str, Union[Validator, Callable[[Any], None]]]


class Pattern:
    """

    """
    def __init__(self, pattern: PatternType) -> None:
        self._pattern = self._pattern_validation(pattern)

    @property
    def pattern(self) -> PatternType:
        return self._pattern

    def get_validator(self, arg: str) -> Validator:
        v = self._pattern.get(arg)
        if v is None:
            raise PatternError(
                f"There is no validator for this argument: '{arg}'"
            )
        return v

    def __iter__(self) -> Iterator:
        return iter(self._pattern.items())

    @staticmethod
    def _pattern_validation(pattern: PatternType) -> PatternType:
        if not isinstance(pattern, dict):
            raise PatternError(
                f"Patterns must be defined in the form of a dict"
            )
        for a, v in pattern.items():
            if not isinstance(a, str):
                raise PatternError(
                    f"All Pattern keys must be of type str. "
                    f"Received: {a} from {type(a)}"
                )
            if not isinstance(v, Validator):
                if callable(v):
                    pattern[a] = CallableValidator(v)
                    continue
                raise PatternError(
                    "All Pattern values must be of type Validator. "
                    f"Received: {v} from {type(v)}"
                )
        return pattern

    def match(self, callable_: Callable, *args, **kwargs) -> Pattern:
        args = getcallargs(
            callable_,
            *args,
            **kwargs
        )
        for param, _ in self:
            if param not in args.keys():
                raise PatternError(
                    "Pattern does not match callable. "
                    f"There is no parameter named '{param}' in callable"
                )
        return self