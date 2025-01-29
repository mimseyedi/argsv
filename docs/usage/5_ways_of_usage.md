There are various methods and approaches for **validating arguments**, and as a programmer, you have a lot of **flexibility** in this regard. **argsv** is not meant to impose limitations or restrict your options. It strives, as much as possible, to utilize structures and tools that can be applied in diverse and different ways.  

Nevertheless, in this topic, we are going to delve a bit into how to use **argsv** and, in general, how to **validate arguments**.

At first glance, **argsv** and using the `argsval` **decorator** might seem like an **appealing** and **readable** idea. However, to avoid **complex** and **combined validations** while keeping the validation-related code concise and **readable** in the **argsv** style, we can use the following approach:

1. Assign a specific file for the [validators](https://github.com/mimseyedi/argsv/wiki/3.-Validators).  
2. Design the **validators** as **functions** and leverage **argsv**'s [built-in validators](https://github.com/mimseyedi/argsv/wiki/3.-Validators#34-built-in-validators-).  
3. Use the [argsval](https://github.com/mimseyedi/argsv/wiki/2.-Validation-Process#23-validation-by-decorator-) **decorator** and the implemented **validators**.  

Let's look at an example together:

Suppose we have a module containing implemented functions. 

```python
# dummy_module.py

def div(a, b):
    return a / b


def get_ascii_code(char):
    return ord(char)


def iterate(*iterables):
    for it in iterables:
        yield from it
```

First, we create a **file** for our [validators](https://github.com/mimseyedi/argsv/wiki/3.-Validators) and **implement** them based on the **parameters** of our **functions**.

```python
# validators.py
from typing import Iterable
from argsv.validators import multival, typeval, eq, ne


def div_pattern():
    number_type = typeval(
        (int, float)
    )
    validation_pattern = {
        'a': number_type,
        'b': multival(number_type, ne(0)),
    }
    return validation_pattern


def char_validator(char):
    validator = multival(
        typeval(str),
        eq(1, key=len)
    )
    validator(char)


def iterables_validator(iterables):
    for i, it in enumerate(iterables):
        if not isinstance(it, Iterable):
            raise TypeError(
                f"Non-Iterable object, at index {i}"
            )
```

As you can see, we **implemented** our [validators](https://github.com/mimseyedi/argsv/wiki/3.-Validators) in different ways—sometimes **independently**, sometimes with the help of argsv's [built-in validators](https://github.com/mimseyedi/argsv/wiki/3.-Validators#34-built-in-validators-), and sometimes by returning a [validation pattern](https://github.com/mimseyedi/argsv/wiki/2.-Validation-Process#22-validation-pattern-). Now, we can use them like this:

```python
# dummy_module.py
from argsv import argsval
from validators import *


@argsval(**div_pattern())
def div(a, b):
    return a / b


@argsval(char=char_validator)
def get_ascii_code(char):
    return ord(char)


@argsval(iterables=iterables_validator)
def iterate(*iterables):
    for it in iterables:
        yield from it
```

As you can see, with this **approach** and **structure**, not only is the [validation process](https://github.com/mimseyedi/argsv/wiki/2.-Validation-Process) carried out in a more **organized** and **separated** manner from the main body of the function, but it is also more **readable** and **simpler**.  

You can also use the [built-in validators](https://github.com/mimseyedi/argsv/wiki/3.-Validators#34-built-in-validators-) directly **within** the function body for **internal** and direct **validations**, if you prefer. Alternatively, you can define your own [validation patterns](https://github.com/mimseyedi/argsv/wiki/2.-Validation-Process#22-validation-pattern-) as **constants** in a separate file and use them as needed.  

In any case, you have the freedom to choose different **validation methods** and create your own **style**. So, feel free to experiment and develop a pattern that suits you best!