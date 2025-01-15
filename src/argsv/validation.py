"""

"""


from typing import(
    Any,
    Dict,
    Tuple,
    Callable,
)
from functools import wraps
from inspect import getcallargs

from _pattern import Pattern, PatternType
from errors import ValidationError


class ArgsVal:
    """

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
        args = getcallargs(
            self._callable,
            *self._args,
            **self._kwargs,
        )
        for name, v in self.pattern:
            a = args.get(name)
            try:
                v(a)
            except BaseException as e:
                raise ValidationError(
                    (
                        "Validation stopped while checking "
                        f"the argument passed to parameter '{name}'\n"
                        f"From validator: {v.name}\n"
                        f" └── {type(e).__name__}: {e}"
                    )
                ) from None

    def _verify_pattern(self, pattern: PatternType) -> Pattern:
        return Pattern(
            pattern
        ).match(
            self._callable,
            *self._args,
            **self._kwargs,
        )

    @staticmethod
    def _check_callable(callable_: Callable) -> Callable:
        if not callable(callable_):
            err_msg = (
                f"'{type(callable_).__name__}' "
                "object is not callable"
            )
            raise TypeError(err_msg)
        return callable_


def argsval(**pattern) -> Callable:
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