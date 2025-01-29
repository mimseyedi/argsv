"""
@rgs✔

This file is about the basics of Validators.
By implementing a base and abstract class 'Validator'
and controlling and managing similar properties,
it is possible to define and customize Validators.

In this file, built-in Validators such as::

    CallVal
    MultiVal
    IterVal
    TypeVal
    FromTo
    CompVal
    ContainsVal

are implemented by inheriting from 'Validator'.
These validators are implemented to be used and
perform common and required validations easily.

For standard use of these Validators, refer to::

    from argsv.validators import ...

For a better experience and easier use of these
built-in validators, please utilize their interfaces
in the mentioned path above.
"""


# Standard imports
from abc import (
    ABC,
    abstractmethod,
)
from typing import(
    Any,
    Dict,
    Type,
    Tuple,
    Union,
    Optional,
    Callable,
    Iterable,
    Iterator,
    Container,
)
from inspect import signature
# Internal imports
from .errors import (
    ValidatorError,
    ValidationError,
    ValidationKeyError,
)


# Defining a type for Key
# A callable or attrubute in 'str' format
KeyType = Optional[
    Union[Callable, str]
]
# Defining a type for Callable
# A callable with one parameter
# And with an output of 'None' or 'bool'
CallableType = Callable[
    [Any], Optional[bool]
]


class Validator(ABC):
    """
    The Validator class is an abstract base class
    that can be inherited to implement standard Validators.

    This class allows other Validators to be easily implemented
    by controlling and managing properties such as
    `exception type`, `exception message`, `validation key`, and its `arguments`.

    Also, each Validator is required to implement a property
    called `name` to refer to the name of the Validator,
    and its validation process must be performed in the
    `__call__` dunder method, like a callable object.

    :param exc: Exception type
    :param exc_msg: Exception message
    :param key: Validation key (callable | attribute)
    :param args: Validation key args
    :param kwargs: Validation key kwargs
    :param aloc: The location of arg in Validation key
    """

    def __init__(
        self,
        exc: Optional[Type[BaseException]] = None,
        exc_msg: Optional[str] = None,
        *,
        key: KeyType = None,
        args: Optional[Tuple[Any, ...]] = None,
        kwargs: Optional[Dict[str, Any]] = None,
        aloc: Optional[int] = None,
    ) -> None:
        self._exc = self._exc_validation(exc)
        self._exc_msg = self._exc_msg_validation(exc_msg)
        self._key = self._key_validation(key)
        self._args = self._args_validation(args)
        self._kwargs = self._kwargs_validation(kwargs)
        self._aloc = self._aloc_validation(aloc)

    @property
    def exc(self) -> Type:
        return self._exc

    @property
    def exc_msg(self) -> Optional[str]:
        return self._exc_msg

    @property
    def key(self) -> KeyType:
        return self._key

    @property
    def args(self) -> Optional[Tuple[Any, ...]]:
        return self._args

    @property
    def kwargs(self) -> Optional[Dict[str, Any]]:
        return self._kwargs

    @property
    def aloc(self):
        return self._aloc

    @property
    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def __call__(self, arg: Any) -> None:
        pass

    @staticmethod
    def _get_key(
        arg: Any,
        key: KeyType,
        args: Optional[Tuple[Any, ...]] = None,
        kwargs: Optional[Dict[str, Any]] = None,
        aloc: Optional[int] = None,
    ) -> Any:
        """
        The validation process can be changed
        by a validation key from the pure value
        of an argument to the value of a callable
        with the argument or a attribute of the argument.

        This method returns the expected value
        if the validation key is set, and the value
        of the argument itself if the validation key
        is not set.

        The following is an example to show how to validate
        the length of an argument using `argsv` validators::

            from argsv import argsval
            from argsv.validators import eq
            @argsval(a=eq(3, key=len))
            def dummy(a: list):
                return a

        Here, instead of validating the argument,
        its length is validated and if it is `equal to 3`,
        it is accepted.

        If you are using a function as a validation key
        that does not take the argument being validated
        as the first input, you can specify the location
        where the argument should be sent with the 'aloc' parameter::

            from argsv import argsval
            from argsv.validators import iterval, eq
            @argsval(
                a=iterval(
                    eq(10),
                    key=filter,
                    args=(lambda x: x > 5,),
                    aloc=1,
                )
            )
            def dummy(a):
                return a

        In this example, since the `filter` takes an iterable
        as its second input, the argument `a` is sent
        to the second parameter of `filter` as
        a validation key using the `aloc` assignment.

        :param arg: Argument
        :param key: Validation key (callable | attribute)
        :param args: Key args
        :param kwargs: Key kwargs
        :param aloc: The location of arg in Validation key
        :return: Any
        """

        # This internal function is responsible for
        # placing the argument relative to the position
        # specified in positional arguments.
        def _arg_placement(arg_, loc_, args_):
            base, alen = 0, len(args_)
            # Argument position validation
            if loc_ > len(args_) or loc_ < base:
                err_msg_ = (
                    f"The location where "
                    f"argument should be "
                    f"placed is out of range."
                )
                raise ValidationKeyError(err_msg_)
            # Creating an iterator
            ait = iter(args_)
            # Iterate over positional arguments,
            # place arguments between them,
            for i in range(alen + 1):
                yield arg_ if i == loc_ else next(ait)

        # If validation key is not set,
        # 'arg' itself will be returned
        if key is None:
            return arg
        # Validating args and kwargs
        c = 0
        for a, t in zip(
            (args, kwargs,),
            (tuple, dict,),
        ):
            # Initialization
            if a is None:
                if c == 0:
                    args = tuple()
                else:
                    kwargs = dict()
            # Checking types
            elif not isinstance(a, t):
                err_msg = (
                    f"{a} is not of type "
                    f"'{type(t).__name__}'"
                )
                raise ValidationKeyError(err_msg)
            c += 1

        # Attribute validation
        if isinstance(key, str):
            try:
                attr = getattr(arg, key)
            except AttributeError as e:
                raise ValidationKeyError(e) from None
            else:
                if isinstance(attr, Callable):
                    try:
                        if aloc is not None:
                            r = attr(
                                *_arg_placement(
                                    arg,
                                    aloc,
                                    args,
                                ),
                                **kwargs,
                            )
                        else:
                            r = attr(*args, **kwargs)
                    except BaseException as e:
                        raise ValidationKeyError(e) from None
                    else:
                        return r
                return attr
        # Callable validation
        elif isinstance(key, Callable):
            try:
                if aloc is not None:
                    res = key(
                        *_arg_placement(
                            arg,
                            aloc,
                            args,
                        ),
                        **kwargs,
                    )
                else:
                    res = key(
                        arg,
                        *args,
                        **kwargs,
                    )
            except BaseException as e:
                raise ValidationKeyError(e) from None
            else:
                return res

    @staticmethod
    def _exc_validation(
        exc: Optional[Type[BaseException]],
    ) -> Type:
        """
        This method validates the exception type and,
        if confirmed, returns the exception itself.

        :param exc: Exception type
        :return: Type[BaseException]
        """

        if exc is None:
            return ValidationError
        if not (
            isinstance(exc, BaseException)
            or
            (
                isinstance(exc, type)
                and
                issubclass(exc, BaseException)
            )
        ):
            raise TypeError
        return exc

    @staticmethod
    def _exc_msg_validation(
        exc_msg: Optional[str],
    ) -> Optional[str]:
        """
        This method validates the exception message and,
        if confirmed, returns the message itself.

        :param exc_msg: Exception message
        :return: str
        """

        if exc_msg is None or \
            isinstance(exc_msg, str):
            return exc_msg
        raise TypeError

    @staticmethod
    def _key_validation(key: KeyType) -> KeyType:
        """
        This method validates the validation key and,
        if confirmed, returns the key itself.

        :param key: Validation key
        :return: KeyType
        """

        if isinstance(key, KeyType):
            return key
        raise TypeError

    @staticmethod
    def _args_validation(
        args: Optional[Tuple[Any, ...]]
    ) -> Optional[Tuple[Any, ...]]:
        """
        This method validates the key validation args and,
        if confirmed, returns the args itself.

        :param args: Key validation args
        :return: Tuple[Any, ...]
        """

        if args is None or \
            isinstance(args, tuple):
            return args
        raise TypeError

    @staticmethod
    def _kwargs_validation(
        kwargs: Optional[Dict[str, Any]]
    ) -> Optional[Dict[str, Any]]:
        """
        This method validates the key validation kwargs and,
        if confirmed, returns the kwargs itself.

        :param kwargs: Key validation kwargs
        :return: Dict[str, Any]
        """

        if kwargs is None or \
                isinstance(kwargs, dict):
            return kwargs
        raise TypeError

    def _aloc_validation(
        self,
        aloc: Optional[int],
    ) -> Optional[int]:
        """
        This method validates the `aloc`
        (location of arg in Validation key)
        and, if confirmed, returns the `aloc` itself.

        :param aloc: The location of arg in Validation key
        :return: int | None
        """

        if self._key is None and \
            aloc is not None:
            err_msg = (
                "Argument location cannot "
                "be set if 'key' is not set."
            )
            raise ValidatorError(err_msg)
        return aloc


class CallVal(Validator):
    """
    The `CallVal` class is a Validator that performs validation
    upon receiving a callable.
    If the return value of the callable is `False`,
    the validation fails, otherwise the callable itself
    is responsible for generating the error.

    :param callable_: Callable object
    :param args: exc, exc_msg
    :param kwargs: key, args, kwargs
    """

    def __init__(
        self,
        callable_: CallableType,
        *args,
        **kwargs,
    ) -> None:
        self._callable = callable_
        super().__init__(*args, **kwargs)

    @property
    def name(self) -> str:
        # Returning the name of the callable
        return self._callable.__name__

    def __call__(self, arg: Any) -> None:
        # Get the value to be validated.
        k = self._get_key(
            arg,
            self.key,
            self.args,
            self.kwargs,
            self.aloc,
        )
        # Get the return value from a callable
        res = self._callable(k)
        # Setting the exception and default message
        # if the callable result is `False`
        if res is False:
            # Get the value of exc_msg
            err_msg = self.exc_msg
            # Set a default message
            if err_msg is None:
                err_msg = (
                    "Validation failed due to return "
                    f"False from validator {self._callable}"
                )
            raise self.exc(err_msg)

    @staticmethod
    def _callable_validation(
            callable_: CallableType
    ) -> CallableType:
        """
        This method is responsible for validating a callable.
        If the callable itself is validated, it will be returned.

        :param callable_: Callable object
        :return: CallableType
        """

        # Checking type
        if not callable(callable_):
            err_msg = (
                f"'{type(callable_).__name__}' "
                "object is not callable"
            )
            raise ValidatorError(err_msg)

        # Does callable have only one parameter?
        sig = signature(callable_)
        if len(sig.parameters) == 1:
            return callable_

        err_msg = (
            f"Callable '{callable_.__name__}' "
            "can only have one parameter"
        )
        raise ValidatorError(err_msg)

    def __repr__(self):
        return f"CallableValidator({self._callable})"


class MultiVal(Validator):
    """
    This Validator, by receiving other Validators, is responsible
    for performing multiple validations. Specifically, `MultiVal`
    behaves like an Iterable and has the ability to perform
    multiple validations for a single argument.

    :param validators: Validator | Callable
    """

    def __init__(
        self,
        *validators: Union[Validator, Callable],
    ) -> None:
        self._name = None
        self._validators = validators
        super().__init__()

    @property
    def name(self) -> str:
        return self._name

    def __iter__(self) -> Iterator:
        return iter(self._validators)

    def __call__(self, arg: Any) -> None:
        # Iterating into validators
        for i, v in enumerate(self, 1):
            # If they are just a callable object
            # they become a Validator
            if callable(v) and \
                not isinstance(v, Validator):
                v = CallVal(v)
            # The name and position of validators
            # are preserved in the validation process
            self._name = (
                f"multival('{v.name}' "
                f"in position {i})"
            )
            # validator is called for validation
            v(arg)

    @staticmethod
    def _validators_validation(
        iterable: Iterable
    ) -> Iterable:
        """
        The task of this method is to validate
        an Iterable of Validators.
        If verified, it will return the iterable itself.

        :param iterable: Iterable object
        :return: Iterable
        """

        # Checking type
        if not isinstance(iterable, Iterable):
            err_msg = (
                f"'{type(iterable).__name__}' "
                "object is not iterable"
            )
            raise ValidatorError(err_msg)

        # Checking Iterable values
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

    def __repr__(self):
        return f"MultiVal({tuple(self)})"


class IterVal(Validator):
    """
    The `IterVal` class is used to create Validators
    that are supposed to validate Iterables.
    These Validators validate all items against a given
    Validator by moving through the Iterable they receive.
    """

    def __init__(
        self,
        validator: Union[Validator, CallableType],
        *args,
        **kwargs,
    ) -> None:
        self._name = None
        self._validator = validator
        super().__init__(*args, **kwargs)

    @property
    def name(self) -> str:
        return self._name

    def __call__(self, arg: Any) -> None:
        # Get the value to be validated.
        k = self._get_key(
            arg,
            self.key,
            self.args,
            self.kwargs,
            self.aloc,
        )
        # Checking type
        if not isinstance(k, Iterable):
            err_msg = (
                f"'{type(k).__name__}' "
                "object is not iterable"
            )
            raise ValidatorError(err_msg)

        # Get validator
        v = self._validator

        # If they are just a callable object
        # they become a Validator
        if callable(v) and \
            not isinstance(v, Validator):
            v = CallVal(v)

        try:
            # Validation process
            for i, item in enumerate(k):
                # Setting a name (err_msg)
                self._name = (
                    f"iterval(Corruption at "
                    f"index: {i}, item: '{item}')"
                )
                # Calling validator
                # and validate iterable values
                v(item)
        # Handling validation error
        except ValidationError:
            raise
        # Handling validation key error
        except BaseException as e:
            self._name = (
                "iterval(Error in validation key)"
            )
            raise ValidatorError(e) from None

    @staticmethod
    def _validator_validation(
        validator: Union[Validator, CallableType]
    ) -> Union[Validator, CallableType]:
        """
        The task of this method is to validate
        a Validator. If verified,
        it will return the validator itself.

        :param validator: A validator or callable
        :return: Validator | CallableType
        """

        if not isinstance(
            validator,
            (Validator, CallableType,),
        ):
            err_msg = (
                "iterval only accepts "
                "'Validator' and 'CallableType', "
                f"Received: {type(validator)}"
            )
            raise ValidatorError(err_msg)
        return validator

    def __repr__(self):
        return f"IterVal({self._validator})"


class TypeVal(Validator):
    """
    The `TypeVal` class is a validator for checking
    the type of arguments.
    This class behaves just like the built-in 'isinstance' function
    and can be passed a specific `type`, a `tuple of types`, or a `Union`.

    :param type_: type | Tuple[type, ...] | Union
    :param args: exc, exc_msg
    :param kwargs: key, args, kwargs
    """

    def __init__(
        self,
        type_: Union[type, Tuple[type, ...]],
        *args,
        **kwargs,
    ) -> None:
        self._type = type_
        super().__init__(*args, **kwargs)

    @property
    def name(self):
        # The name of the interface validator
        # will be returned from `argsv.validators`
        return type(self).__name__.lower()

    def __call__(self, arg: Any) -> None:
        # Get the type
        t = self._type
        # Get the value to be validated.
        k = self._get_key(
            arg,
            self.key,
            self.args,
            self.kwargs,
            self.aloc,
        )
        try:
            # Checking type
            if not isinstance(k, t):
                # Get the value of exc_msg
                err_msg = self.exc_msg
                # Set a default message
                if err_msg is None:
                    err_msg = (
                        f"Expected type is "
                        f"'{self._get_ftype(t)}', "
                        f"But received: '{type(k).__name__}'"
                    )
                raise self.exc(err_msg)
        # Error handling
        except TypeError:
            err_msg = (
                "typeval() arg 1 must be a type, "
                "a tuple of types, or a union"
            )
            raise ValidatorError(err_msg)

    @staticmethod
    def _get_ftype(
        type_: Union[type, Tuple[type, ...]]
    ) -> str:
        """
        This method accepts different types,
        formats them in a readable way, and
        returns them in `str` format.

        :param type_: type | Tuple[type, ...] | Union
        :return: str
        """
        if isinstance(type_, type):
            return type_.__name__
        if isinstance(type_, tuple):
            t = map(
                lambda t_: t_.__name__,
                type_,
            )
            return f"({', '.join(t)})"
        return type_.__str__()

    def __repr__(self):
        return f"TypeVal({self._get_ftype(self._type)})"


class FromTo(Validator):
    """
    The `FromTo` class is a Validator for validating
    arguments within a specific numeric range.
    This class is used with its Validator interface in
    `argsv.validators` and can be used to check an argument
    within a specific range.

    `Note: The FromTo validator only works with numbers.`

    :param from_: from (<'int'> | <'float'>)
    :param to_: to (<'int'> | <'float'>)
    :param args: exc, exc_msg
    :param kwargs: key, args, kwargs
    """

    def __init__(
        self,
        from_: Union[int, float],
        to_: Union[int, float],
        *args,
        **kwargs,
    ):
        self._from = self._num_validation(from_)
        self._to = self._num_validation(to_)
        super().__init__(*args, **kwargs)

    @property
    def name(self) -> str:
        # The name of the interface validator
        # will be returned from `argsv.validators`
        return type(self).__name__.lower()

    def __call__(self, arg: Any) -> None:
        # Get the value to be validated.
        k = self._get_key(
            arg,
            self.key,
            self.args,
            self.kwargs,
            self.aloc,
        )
        # Type checking the value
        # returned from the validation key
        if not isinstance(k, (int, float)):
            err_msg = (
                "Only numbers (<'int'>, <'float'>) "
                "are acceptable, "
                "But the selected key returns an "
                f"'{type(k).__name__}'"
            )
            raise ValidatorError(err_msg)

        # Condition definition
        c = k in self

        if not c:
            # Get the value of exc_msg
            err_msg = self.exc_msg
            # Set a default message
            if err_msg is None:
                err_msg = (
                    f"{k} is not between "
                    f"{self._from} and {self._to}"
                )
            raise self.exc(err_msg)

    def __contains__(self, item: Union[int, float]) -> bool:
        return self._from <= item <= self._to

    @staticmethod
    def _num_validation(n: Any) -> Union[int, float]:
        """
        The task of this method is to validate
        the inputs of the class.
        The inputs must be of type number (<'int'> | <'float'>).

        :param n: Any object
        :return: Union[int, float]
        """

        if isinstance(n, Union[int, float]):
            return n
        err_msg = (
            "The fromto validator only "
            "works with numbers (<'int'>, <'float'>)"
        )
        raise ValidatorError(err_msg)

    def __repr__(self):
        return f"FromTo({self._from}, {self._to})"


class CompVal(Validator):
    """
    The `CompVal` class is used to create comparison validators.
    Validators that validate and compare arguments with another value.

    The validators interface of this class in argsv.validators::

        eq -> Equality comparison
        ne -> Inequality comparison
        gt -> A comparison of greater-than
        lt -> A comparison of less-than
        ge -> Comparison greater-than-or-equal to
        le -> Comparison less-than-or-equal to

    :param other: The object to be compared with
    :param action: Comparison action
    :param args: exc, exc_msg
    :param kwargs: key, args, kwargs
    """

    def __init__(
        self,
        other: Any,
        action: str,
        *args,
        **kwargs,
    ) -> None:
        self._other = other
        self._name = None
        self._action = self._action_validation(action)
        super().__init__(*args, **kwargs)

    @property
    def name(self):
        return self._name

    def __call__(self, arg: Any) -> None:
        # Get the value to be validated.
        k = self._get_key(
            arg,
            self.key,
            self.args,
            self.kwargs,
            self.aloc,
        )
        # Get comparison result
        # and error message
        b, m = self.compare(
            k,
            self._other,
            self._action
        )
        # If the comparison result is 'False'
        if not b:
            # Get the value of exc_msg
            err_msg = self.exc_msg
            # Setting the error message
            # with the received message
            if err_msg is None:
                err_msg = m
            raise self.exc(err_msg)

    @staticmethod
    def compare(a: Any, b: Any, opr: str) -> Union[Tuple, None]:
        """
        The task of this method is to perform
        a comparison operation using comparison operators.
        The return value is a tuple of the
        comparison result and the error message.

        :param a: Any object
        :param b: Any object
        :param opr: Comparison operator
        :return: Union[Tuple, None]
        """

        try:
            return {
                "==": (
                    a == b,
                    f"{a} is not equal to {b}",
                ),
                "!=": (
                    a != b,
                    f"{a} is equal to {b}, not unequal",
                ),
                ">": (
                    a > b,
                    f"{a} is not greater-than {b}",
                ),
                "<": (
                    a < b,
                    f"{a} is not less-than {b}",
                ),
                ">=": (
                    a >= b,
                    f"{a} is not greater-than-or-equal-to {b}",
                ),
                "<=": (
                    a <= b,
                    f"{a} is not less-than-or-equal-to {b}",
                )
            }.get(opr, None)

        # Handling comparison errors
        except TypeError:
            err_msg = (
                f"Instances of '{type(a).__name__}' and "
                f"'{type(b).__name__}' are not comparable."
            )
            raise ValidatorError(err_msg) from None

    def _action_validation(self, action: str) -> str:
        """
        The task of this method is to validate
        the comparison action.
        Each comparison operation can only be
        considered in the following cases::

            ("==", "!=", ">", "<", ">=", "<=")

        :param action: Comparison action
        :return: str
        """

        # Associating actions with
        # their validator interface names
        name = {
            "==": "eq",
            "!=": "ne",
            ">" : "gt",
            "<" : "lt",
            ">=": "ge",
            "<=": "le"
        }.get(action, None)

        # If there was action
        if name is not None:
            # Setting the name
            self._name = name
            return action

        err_msg = (
            "No such action is defined "
            f"for comparison operations: "
            f"'{action}'"
        )
        raise ValidatorError(err_msg)

    def __repr__(self):
        return f"{self.name}({self._other})"


class ContainsVal(Validator):
    """
    The `ContainsVal` class is implemented to create validators
    that are supposed to validate the existence of
    an argument within a container.

    This class takes a container and checks whether the argument
    being validated is present within it or not.

    There is also a parameter called `not_` which reverses
    the validation and its default value is `False`.
    """

    def __init__(
        self,
        container: Container,
        not_: Optional[bool]=False,
        *args,
        **kwargs,
    ) -> None:
        self._container = self._container_validation(container)
        self._not = bool(not_)
        super().__init__(*args, **kwargs)

    @property
    def name(self) -> str:
        # Set name, considering, `self._not`
        return "inval" if not self._not else "notinval"

    def __call__(self, arg: Any) -> None:
        # Get the value to be validated
        k = self._get_key(
            arg,
            self.key,
            self.args,
            self.kwargs,
            self.aloc,
        )

        # Condition definition
        c = k in self._container
        b = not c if self._not else c

        if not b:
            # Get the value of exc_msg
            err_msg = self.exc_msg
            # Set a default message
            if err_msg is None:
                # if 'in'
                if self._not:
                    err_msg = (
                        f"{k} exists as an "
                        f"item in {self._container}"
                    )
                # if 'not in'
                else:
                    err_msg = (
                        f"{k} does not exist as "
                        f"an item in {self._container}"
                    )
            raise self.exc(err_msg)

    @staticmethod
    def _container_validation(
        container: Container,
    ) -> Container:
        """
        The task of this method is to validate
        the main-input of the class.
        The input must be of type `<'Container'>`.

        :param container: A container object
        :return: Container
        """

        if isinstance(container, Container):
            return container
        err_msg = (
            f"{container} is not container"
        )
        raise ValidatorError(err_msg)

    def __repr__(self):
        return f"{self.name}({self._container})"