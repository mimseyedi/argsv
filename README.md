[![pypi](https://img.shields.io/pypi/v/argsv.svg)](https://pypi.org/project/argsv/) [![support-version](https://img.shields.io/pypi/pyversions/argsv)](https://img.shields.io/pypi/pyversions/argsv) [![license](https://img.shields.io/github/license/mimseyedi/argsv.svg)](https://github.com/mimseyedi/argsv/blob/master/LICENSE) [![commit](https://img.shields.io/github/last-commit/mimseyedi/argsv)](https://github.com/mimseyedi/argsv/commits/master)

![](https://raw.githubusercontent.com/mimseyedi/argsv/master/docs/images/argsv-poster.png)

## Introduction
**argsv** is a library for validating arguments passed to callables. With this library, you can validate arguments sent to callables in a simpler, more readable, and well-defined context.

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
* [Getting started](#getting_started)
* [Why argsv?](#why_argsv)
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

## Getting started <a class="anchor" id="getting_started"></a>
Hello! As the creator and primary developer of **argsv**, I’ve often felt that validating the arguments passed to a callable object directly within its body can be somewhat unpleasant. Personally, and perhaps for many others, I prefer the code within the body of a function to remain clean, focused, and directly related to its primary purpose. Including argument validation at the start of a function’s body doesn’t always look appealing and, at least for my perfectionist mind, lacks elegance.

Some might argue that in Python, argument validation isn’t always a necessity. In many cases, I agree with this perspective, as Python aims to accelerate implementation and development. However, there are certain scenarios—like when developing a module or library, or working on a specific project intended for use by others—where argument validation and generating precise errors become crucial. These practices help us act more responsibly when providing tools for others to use.

All these considerations led me to the idea of creating **argsv**. My primary goal was to separate the validation process from the core logic of a function, making it simpler and more readable (hopefully, I’ve succeeded!).

To achieve this, I turned to **decorators** and designed a structure where argument validation could happen outside the body of the function. 

```python
from argsv import argsval

@argsval(b=lambda x: x != 0)
def div(a, b):
    return a / b
```

For instance, using the `argsval` decorator along with a lambda-based callable validator, I can define that the argument passed to parameter b must not be zero.

That said, I also developed the structure in such a way that it remains flexible. For those who, for any reason, prefer to handle argument validation within the function body, this is still entirely possible.

```python
from argsv import ArgsVal

def div(a, b):
    ArgsVal(
      div, {'b': lambda x: x != 0}, a, b
    ).validate()
    # Function code:
    return a / b
```

To understand how to work with **argsv** and access its documentation, you can continue reading or visit the <a href="https://github.com/mimseyedi/argsv/tree/master/docs/usage">docs/usage</a> section.

## Why argsv? <a class="anchor" id="why_argsv"></a>
- **Lightweight**: It doesn't rely on any external modules or libraries.  
- **Readable**: It separates the validation process from the main code, improving clarity.  
- **Simplifies Validation**: Makes the argument validation process easier.  
- **Precise Error Reporting**: Accurately displays errors in the validation process.  
- **Universal Compatibility**: Works with all types of callables.  
- **Built-in Validators**: Provides common and useful built-in validators.  
- **Custom Validators**: Allows you to implement your own customized validators.  
- **Extensible**: Designed to be flexible and expandable.

## Usage <a class="anchor" id="usage"></a>
There are two ways to validate arguments using **argsv**:

- By using a **decorator**.
- By using the **ArgsVal** class and creating an **internal validation** process.

In the following sections, you'll get familiar with both methods and gain a better understanding of the argument validation structure in **argsv**.
## Validation by decorator <a class="anchor" id="validation_by_decorator"></a>
One of the best ways to use **argsv** is through the `argsval` decorator. By using this **decorator** and moving the argument validation process outside the body of the callable, your code becomes more readable, and the validation process takes place in its own dedicated section, separate from the main logic of the callable.  

The `argsval` decorator relies on <a href="#validation_pattern">**validation pattern**</a> to validate arguments. These **patterns** are **dictionaries** where the **keys** represent the names of the **parameters** (to which the arguments are passed), and the **values** are the <a href=#validators>**validators**</a>.  

You can use the `argsval` decorator to validate specific arguments by passing **keyword arguments** and assigning them a **validator**.

```python
from argsv import argsval

def check_seq(seq):
    for item in seq:
        if not isinstance(item, int):
            raise TypeError(
              "Sequence items must be of type int. "
              f"'{item}' is not an 'int' object"
            )
   
@argsval(seq=check_seq)
def square(seq):
    for num in seq:
        yield num ** 2
```

In this example, the `check_seq` function acts as a <a href=#callable_validators>**callable validator**</a> that validates the type of items within a sequence. Using the `argsval` decorator, it is designated as the **validator** for validating the argument passed to the `seq` **parameter** of the `square` generator.

For example, I iterate through the `square` generator and intentionally define one of the items in the sequence with the type `str`. When the program runs, **argsv** provides detailed information about the validation process failure.

```python
for x in square([1, 2, 'OPS', 3]):
    print(x)
```

Output:
```
ValidationError: Validation stopped while checking the argument passed to parameter 'seq', in callable 'square'
From validator: check_sequence
 └── TypeError: Sequence items must be of type int. 'OPS' is not an 'int' object
```
Here, `argsval` raises a `ValidationError`, indicating that the validation process failed and was interrupted while checking the argument passed to the `seq` parameter. Additionally, the validator responsible for this validation, along with the error message, is clearly specified.

## Internal validation <a class="anchor" id="internal_validation"></a>
The argument validation process is also accessible for those who prefer to handle it within the function body! By importing the `ArgsVal` class, you can create an instance of this class by passing a **callable** object along with its **arguments** and a <a href=#validation_pattern>**validation pattern**</a>. Then, by calling the `validate` method, you can perform the validation process.

```python
from argsv import ArgsVal

def check_weight(weight):
    if not isinstance(weight, (int, float)):
        raise TypeError("Weight must be a number")
    if weight < 0:
        raise ValueError("Weight cannot be negative")

def lbs_to_kg(weight):
    ArgsVal(
      lbs_to_kg, {"weight": check_weight}, weight
    ).validate()
    return weight * 0.453592
```

## Validation pattern <a class="anchor" id="validation_pattern"></a>

## Validators <a class="anchor" id="validators"></a>

## Callable validators <a class="anchor" id="callable_validators"></a>

## Custom validators <a class="anchor" id="custom_validators"></a>

## Built-in validators <a class="anchor" id="built-in_validators"></a>

## Bugs/Requests <a class="anchor" id="bugs-requests"></a>

## License <a class="anchor" id="license"></a>