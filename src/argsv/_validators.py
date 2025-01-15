"""

"""


from abc import (
    ABC,
    abstractmethod,
)
from typing import(
    Any,
    Optional,
    Callable,
    Iterable,
)
from inspect import signature

from errors import (
    ValidatorError,
    DefaultValidationError,
)


CallableType = Callable[[Any], Optional[bool]]


class Validator(ABC):
    """

    """

    @property
    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def __call__(self, arg: Any) -> None:
        pass


class CallableValidator(Validator):
    """

    """

    def __init__(self, callable_: CallableType) -> None:
        self._callable = self._callable_validation(callable_)

    @property
    def callable(self) -> CallableType:
        return self._callable

    @property
    def name(self) -> str:
        return self._callable.__name__

    def __call__(self, arg: Any) -> None:
        res = self._callable(arg)
        if res is False:
            raise DefaultValidationError(
                "Validation failed due to return "
                f"False from validator {self._callable}"
            )

    @staticmethod
    def _callable_validation(
        callable_: CallableType
    ) -> CallableType:
        if not callable(callable_):
            err_msg = (
                f"'{type(callable_).__name__}' "
                "object is not callable"
            )
            raise ValidatorError(err_msg)
        
        sig = signature(callable_)
        if len(sig.parameters) == 1:
            return callable_
        
        err_msg = (
            f"Callable '{callable_.__name__}' "
            "can only have one parameter"
        )
        raise ValidatorError(err_msg)


class IterableValidator(Validator):
    def __init__(self, iterable: Iterable) -> None:
        self._iterable = self._iterable_validation(iterable)
        self._name = None

    @property
    def iterable(self):
        return self._iterable

    @property
    def name(self):
        return self._name

    def __call__(self, arg: Any) -> None:
        for i, v in enumerate(self._iterable, 1):
            if callable(v) and \
                not isinstance(v, Validator):
                v = self._convert_call_to_val(v)
            self._name = (
                f"IterableValidator('{v.name}' "
                f"in position {i})"
            )
            v(arg)

    @staticmethod
    def _convert_call_to_val(c: Callable) -> Validator:
        return CallableValidator(c)

    @staticmethod
    def _iterable_validation(
        iterable: Iterable
    ) -> Iterable:
        if not isinstance(iterable, Iterable):
            err_msg = (
                f"'{type(iterable).__name__}' "
                "object is not iterable"
            )
            raise ValidatorError(err_msg)

        for v in iterable:
            if not isinstance(v, Validator) and \
                not callable(v):
                err_msg = (
                    "Iterable values can only "
                    "be Validators or Callables. "
                    f"Received: {v} from {type(v)}"
                )
                raise ValidatorError(err_msg)
        return iterable