[![pypi](https://img.shields.io/pypi/v/argsv.svg)](https://pypi.org/project/argsv/) [![support-version](https://img.shields.io/pypi/pyversions/argsv)](https://img.shields.io/pypi/pyversions/argsv) [![license](https://img.shields.io/github/license/mimseyedi/argsv.svg)](https://github.com/mimseyedi/argsv/blob/master/LICENSE) [![commit](https://img.shields.io/github/last-commit/mimseyedi/argsv)](https://github.com/mimseyedi/argsv/commits/master)

![](https://raw.githubusercontent.com/mimseyedi/argsv/master/docs/images/argsv-poster.png)

## Getting started
**argsv** is a library for **validating arguments passed to callables**. With this library, you can validate arguments sent to callables in a **simpler**, more **readable**, and **well-defined** context.

```python
from argsv import argsval

@argsval(b=lambda x: x != 0)
def div(a, b):
    return a / b
```
Here, with the help of the [argsval decorator](https://github.com/mimseyedi/argsv/wiki/2.-Validation-Process#23-validation-by-decorator-), the operation of the `div` function will only proceed if the argument passed to parameter `b` satisfies the specified **lambda** condition *(i.e., it is not equal to zero)*. Otherwise, the [validation process](https://github.com/mimseyedi/argsv/wiki/2.-Validation-Process) fails, and the corresponding error is raised.

For those who prefer to perform argument validation [within the body of a function](https://github.com/mimseyedi/argsv/wiki/2.-Validation-Process#21-internal-validation-), this option is also available:

```python
from argsv import ArgsVal

def div(a, b):
    ArgsVal(
      div, {'b': lambda x: x != 0}, a, b
    ).validate()
    # Function code:
    return a / b
```

There are [built-in, pre-implemented validators](https://github.com/mimseyedi/argsv/wiki/3.-Validators#34-built-in-validators-) for **common** and **frequently** used validations, which you can easily utilize:

```python
from argsv import argsval
from argsv.validators import multival, typeval, fromto

@argsval(a=multival(typeval(int), fromto(0, 9)))
def dummy(a):
    return a
```

In this example, using the `multival` validator—which allows **multiple validation** operations for a single argument—the **type** of argument `a` is validated by the `typeval` validator, while the **valid range** for parameter `b` is enforced by the `fromto` validator.

📖 *For more information, I recommend checking out the [**argsv documentation**](https://github.com/mimseyedi/argsv/wiki)*.


## Installation
You can use **pip** to install:
```
python3 -m pip install argsv
```

And also to **upgrade**:
```
python3 -m pip install --upgrade argsv
```

## Features
- **Lightweight**: It doesn't rely on any external modules or libraries.  
- **Readable**: It separates the validation process from the main code, improving clarity.  
- **Simplifies Validation**: Makes the argument validation process easier.  
- **Precise Error Reporting**: Accurately displays errors in the validation process.  
- **Universal Compatibility**: Works with all types of callables.  
- **Custom Validators**: Allows you to implement your own customized validators.  
- **Built-in Validators**: Provides common and useful built-in validators.  
- **Extensible**: Designed to be flexible and expandable.


## Bugs/Requests <a class="anchor" id="bugs-requests"></a>
Please send **bug reports** and **feature** requests through <a href="https://github.com/mimseyedi/argsv/issues">Github issue tracker</a>.

## License <a class="anchor" id="license"></a>
**argsv** is a **free** and **open source** project under the **GPL-v3** LICENSE. Any [contribution](https://github.com/mimseyedi/argsv/wiki/6.-Contribution) is welcome. You can do this by **registering** a **pull request**.