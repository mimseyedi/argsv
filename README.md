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