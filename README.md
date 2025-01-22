[![pypi](https://img.shields.io/pypi/v/argsv.svg)](https://pypi.org/project/argsv/) [![support-version](https://img.shields.io/pypi/pyversions/argsv)](https://img.shields.io/pypi/pyversions/argsv) [![license](https://img.shields.io/github/license/mimseyedi/argsv.svg)](https://github.com/mimseyedi/argsv/blob/master/LICENSE) [![commit](https://img.shields.io/github/last-commit/mimseyedi/argsv)](https://github.com/mimseyedi/argsv/commits/master)

![](https://raw.githubusercontent.com/mimseyedi/argsv/master/docs/images/argsv-poster.png)

## Introduction
**argsv** is a library for validating callable object arguments. With the help of **argsv**, you can validate callable object arguments in a separate and distinct manner.

```python
from argsv import argsval

@argsval(b=lambda x: x != 0)
def div(a, b):
    return a / b
```

## Installation
You can use **pip** to install:
```
python3 -m pip install argsv
```

And also to **upgrade**:
```
python3 -m pip install --upgrade argsv
```

## Table of Contents: <a class="anchor" id="contents"></a>
* [Why argsv?](#why_argsv)
  * [Documents](#docs)
* [Usage](#usage)
  * [Validation by decorator](#validation_by_decorator)
  * [Internal validation](#internal_validation)
  * [Validation pattern](#validation_pattern)
* [Validators](#validators)
  * [Callable validators](#callable_validators)
  * [Custom validators](#custom_validators)
  * [Built-in validators](#built-in_validators)
* [Bugs/Requests](#bugs-requests)
* [License](#license)

## Why argsv? <a class="anchor" id="why_argsv"></a>

## Documents <a class="anchor" id="docs"></a>

## Usage <a class="anchor" id="usage"></a>

## Validation by decorator <a class="anchor" id="validation_by_decorator"></a>

## Internal validation <a class="anchor" id="internal_validation"></a>

## Validation pattern <a class="anchor" id="validation_pattern"></a>

## Validators <a class="anchor" id="validators"></a>

## Callable validators <a class="anchor" id="callable_validators"></a>

## Custom validators <a class="anchor" id="custom_validators"></a>

## Built-in validators <a class="anchor" id="built-in_validators"></a>

## Bugs/Requests <a class="anchor" id="bugs-requests"></a>

## License <a class="anchor" id="license"></a>