"""

"""


import re
import pytest

from argsv._pattern import Pattern
from argsv.errors import (
    PatternError,
)
from cases.pattern import *


@pytest.mark.parametrize("case", VALID_PATTERN_ARG_TYPES)
def test_valid_pattern_arg_type(case):
    assert Pattern(case)


@pytest.mark.parametrize("case", INVALID_PATTERN_ARG_TYPES)
def test_invalid_pattern_arg_type(case):
    err_msg = (
        f"Patterns must be defined "
        f"in the form of a 'dict'"
    )
    with pytest.raises(
        PatternError,
        match=re.escape(err_msg),
    ):
        Pattern(case)


@pytest.mark.parametrize("case", VALID_PATTERN_KEYS)
def test_valid_pattern_key(case):
    assert Pattern({case: lambda x: ...})


@pytest.mark.parametrize("case", INVALID_PATTERN_KEYS)
def test_invalid_pattern_key(case):
    err_msg = (
        f"All Pattern keys must "
        f"be of type 'str'. "
        f"Received: {case} from {type(case)}"
    )
    with pytest.raises(
        PatternError,
        match=re.escape(err_msg),
    ):
        Pattern({case: lambda x: ...})


@pytest.mark.parametrize("case", VALID_PATTERN_VALUES)
def test_valid_pattern_value(case):
    assert Pattern({"param": case})


@pytest.mark.parametrize("case", INVALID_PATTERN_VALUES)
def test_invalid_pattern_value(case):
    err_msg = (
        "All Pattern values must "
        "be of type 'Validator'. "
        f"Received: {case} from {type(case)}"
    )
    with pytest.raises(
        PatternError,
        match=re.escape(err_msg)
    ):
        Pattern({"param": case})


@pytest.mark.parametrize("case", VALID_PATTERN_MATCHES)
def test_valid_pattern_match(case):
    c, p = case
    assert Pattern(p).match(c)


@pytest.mark.parametrize("case", INVALID_PATTERN_MATCHES)
def test_invalid_pattern_match(case):
    c, p = case
    err_msg = (
        "Pattern does not match callable. "
        f"There is no parameter "
    )
    with pytest.raises(
        PatternError,
        match=re.escape(err_msg)
    ):
        Pattern(p).match(c)
