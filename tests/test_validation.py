"""

"""


import pytest

from argsv.errors import ValidationError
from cases.validation import *


@pytest.mark.parametrize("case", SUCCESSFUL_VALIDATIONS)
def test_successful_validation(case):
    f, *a = case
    assert f(*a)


@pytest.mark.parametrize("case", FAILED_VALIDATIONS)
def test_failed_validation(case):
    f, *a = case
    with pytest.raises(
        ValidationError
    ): f(*a)
