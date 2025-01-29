![](https://raw.githubusercontent.com/mimseyedi/argsv/master/docs/images/argsv-poster.png)

## Introduction
**argsv** is a library for validating arguments passed to callables. With this library, you can validate arguments sent to callables in a **simpler**, more **readable**, and **well-defined** context.

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

## Table of Contents

* [1. Why **argsv**?](https://github.com/mimseyedi/argsv/wiki/1.-Why-argsv%3F)
* [2. Validation Process](https://github.com/mimseyedi/argsv/wiki/2.-Validation-Process)
  * [2.1. Internal Validation](https://github.com/mimseyedi/argsv/wiki/2.-Validation-Process#21-internal-validation-)
  * [2.2. Validation Pattern](https://github.com/mimseyedi/argsv/wiki/2.-Validation-Process#22-validation-pattern-)
  * [2.3. Validation by Decorator](https://github.com/mimseyedi/argsv/wiki/2.-Validation-Process#23-validation-by-decorator-)
* [3. Validators](https://github.com/mimseyedi/argsv/wiki/3.-Validators)
  * [3.1. Basic Validator](https://github.com/mimseyedi/argsv/wiki/3.-Validators#31-basic-validator-)
    * [3.1.1. Validation Key](https://github.com/mimseyedi/argsv/wiki/3.-Validators#311-validation-key-)
  * [3.2. Custom Validators](https://github.com/mimseyedi/argsv/wiki/3.-Validators#32-custom-validators-)
  * [3.3. Callable Validators](https://github.com/mimseyedi/argsv/wiki/3.-Validators#33-callable-validators-)
  * [3.4. Built-in Validators](https://github.com/mimseyedi/argsv/wiki/3.-Validators#34-built-in-validators-)
* [4. Errors and Reports](https://github.com/mimseyedi/argsv/wiki/4.-Errors-and-Reports)
  * [4.1. PatternError](https://github.com/mimseyedi/argsv/wiki/4.-Errors-and-Reports#41-patternerror-)
  * [4.2. ValidatorError](https://github.com/mimseyedi/argsv/wiki/4.-Errors-and-Reports#42-validatorerror-)
  * [4.3. ValidationKeyError](https://github.com/mimseyedi/argsv/wiki/4.-Errors-and-Reports#43-validationkeyerror-)
  * [4.4. ValidationError](https://github.com/mimseyedi/argsv/wiki/4.-Errors-and-Reports#44-validationerror-)
* [5. Ways of Usage](https://github.com/mimseyedi/argsv/wiki/5.-Ways-of-Usage)
* [6. Contribution](https://github.com/mimseyedi/argsv/wiki/6.-Contribution)