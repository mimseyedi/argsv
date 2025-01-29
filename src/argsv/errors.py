"""
@rgs✔

This file is related to custom argsv errors and exceptions.
This file implements the exceptions that are used and raised
during the validation process.
"""


class ArgsVError(Exception):
    """
    This exception is the most basic exception from
    which all other exceptions inherit.
    """


class ValidationError(ArgsVError):
    """
    This exception occurs when the validation process fails and stops.
    """


class ValidatorError(ArgsVError):
    """
    This exception is related to validators.
    When validators generate their own specific error.
    """


class ValidationKeyError(ValidatorError):
    """
    This exception is raised when an error related
    to the Validation Key occurs.
    """


class PatternError(ArgsVError):
    """
    This exception is related to validation patterns.
    This exception is raised when a pattern does not have
    its correct structure for any reason.
    """