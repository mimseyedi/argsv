**Validators**, in the **argsv** structure, are responsible for **validating** arguments. In a simplified manner, **Validators** are conditions that check for a specific state of an argument. If an argument does not meet the required conditions and is not accepted by the Validator, an exception called [ValidatorError](https://github.com/mimseyedi/argsv/wiki/4.-Errors-and-Reports#42-validatorerror-) is raised, pointing to the **argument** that was not validated.

Validators in **argsv** have a clear definition and structure, which will be explained further below.

## 3.1. Basic Validator <a class="anchor" id="basic_validator"></a>
**Validators** inherit from an abstract base class called [Validator](https://github.com/mimseyedi/argsv/blob/master/src/argsv/_validators.py#L72). This class defines the expected behavior of **Validators** and specifies the components they must **implement**.  

In general, all **Validators** are required to **implement** the `name` property and the `__call__` dunder method. The `name` property refers to the name of the Validator, which is used when generating error messages. The `__call__` method, adhering to the **callable protocol**, makes the **Validator** callable. It accepts an argument (the one to be validated) and performs the validation process on it.

The abstract base class [Validator](https://github.com/mimseyedi/argsv/blob/master/src/argsv/_validators.py#L72), in addition to defining the framework for implementing **Validators**, performs other tasks to make the process of creating Validators **easier** and more **manageable**.  

According to the implementation of this class, **Validators** can **customize** the **error type** and **error message** through the `exc` and `exc_msg` parameters.

For example, by accessing the [Built-in Validators](https://github.com/mimseyedi/argsv/wiki/3.-Validators#34-built-in-validators-) of **argsv** and importing the **pre-implemented** and **ready-to-use** `fromto` **Validator**, as you can see, the argument `a` is validated within a **specified range** (including the start and end points as part of the range). Additionally, the **error type** and **custom message** can be **customized** due to the fact that the `fromto` **Validator** **inherits** from the base abstract class [Validator](https://github.com/mimseyedi/argsv/blob/master/src/argsv/_validators.py#L72).

```python
from argsv import argsval
from argsv.validators import fromto

@argsval(
    a=fromto(
        from_=1, 
        to_=3, 
        exc=ValueError, 
        exc_msg='a is not between 1 and 3!'
    ),
)
def dummy(a):
    return a
```

As expected, if the argument `a` is not between 1 and 3, a `ValueError` will be raised, indicating: *"a is not between 1 and 3!"*.

**Note:** [Built-in Validators](https://github.com/mimseyedi/argsv/wiki/3.-Validators#34-built-in-validators-) will be covered in the following sections.

### 3.1.1 Validation Key <a class="anchor" id="validation_key"></a>
Another feature provided by the abstract base class [Validator](https://github.com/mimseyedi/argsv/blob/master/src/argsv/_validators.py#L72) is the ability to validate arguments using a **Validation Key**. Often, the main value of an argument is not what we aim to validate; instead, we might want to validate a **specific attribute** of the argument or the output of a **function** when the argument is passed to it.

A **Validation Key**, by receiving a **callable** that accepts only one input and passing the argument to be validated to it, enables the validation of the return value of the **specified function** in the **Validation Key** instead of directly validating the main value of the argument.

```python
from argsv import argsval
from argsv.validators import fromto

@argsval(a=fromto(1, 3, key=len))
def dummy(a):
    return a
```

Here, assuming the argument `a` is an object with a measurable **length**, instead of directly validating `a` itself, by passing the `len` function as the **Validation Key**, the **length** of `a` will be validated. It will be approved only if it is **between 1 and 3**.

It is also possible to specify a **string** containing the name of a specific **attribute** of the argument as the **Validation Key**. This allows the value returned by that **attribute** to be validated instead of directly validating the main value of the argument!

```python
from argsv import argsval
from argsv.validators import fromto

@argsval(
    a=fromto(
        1, 
        3, 
        key="__getitem__", 
        args=(0,)
    ),
)
def dummy(a):
    return a
```

In this case, assuming that the argument `a` is a **Sequence**, by specifying the `getitem` dunder method as the **Validation Key** and passing **index zero** as the **positional argument**, instead of validating the value of `a` itself, the value at the **zeroth index** of `a` will be **validated**. It will be validated **successfully** if it falls within the **range of 1 to 3**.

In special cases, when using functions like `filter`, `map`, etc., as the **Validation Key**, the **position** of the argument may not be considered as the **first** parameter. To control this, we can specify the **location** where the argument to be validated should be passed by setting the `aloc` parameter. This allows us to define the **expected** position of the argument in the validation function's **parameter** list.

In this example, using the **built-in validator** `iterval`, which is **pre-implemented** and **ready for use**, we assume that `a` is an **iterable**. Using `filter` as the **Validation Key**, we **filter** through the numbers in `a` that are **greater** than 5. Then, with the help of a **lambda** function, we specify that these numbers must be **even**.

```python
from argsv import argsval
from argsv.validators import iterval

@argsval(
    a=iterval(
        lambda x: x % 2 == 0,
        key=filter,
        args=(lambda x: x > 5,),
        aloc=1,
    ),
)
def dummy(a):
    return a
```

Because the `filter` function takes an **iterable** as its **second** argument, by setting `aloc` to **index 1**, the argument `a` (which is the **iterable**) will be passed as the **second value** to `filter`. This ensures that the validation operates correctly by targeting the correct argument position.


## 3.2. Custom Validators <a class="anchor" id="custom_validators"></a>
You can create **custom validators** by **inheriting** from the abstract base class [Validator](https://github.com/mimseyedi/argsv/blob/master/src/argsv/_validators.py#L72). As mentioned earlier, by inheriting from **Validator**, your class is **required** to implement the `name` property and the `__call__` dunder method.

- In the `name` property, you need to return a specific name for your validator.  
- In the `__call__` dunder method, you perform the validation process by taking the argument to be validated as the only input.

Just as an example, here a custom validator is implemented to validate the type of arguments:

```python
from argsv.validators import Validator


class CustomTypeValidator(Validator):
    def __init__(self, type_, *args, **kwargs):
        self.type = type_
        super().__init__(*args, **kwargs)

    @property
    def name(self):
        return "custom_type_validator"

    def __call__(self, arg):
        if not isinstance(arg, self.type):
            raise TypeError(
                f"{arg} is not an object "
                f"of type {self.type}"
            )
```

In this case, the `CustomTypeValidator` class, by **inheriting** from the abstract and base [Validator](https://github.com/mimseyedi/argsv/blob/master/src/argsv/_validators.py#L72) class, not only receives a `type_` as its **main input** but also the necessary arguments from its **parent** class. It defines the `name` property to specify its **name** and implements the `__call__` method to carry out the **validation operation**.

To get more familiar with the **standard implementation of Custom Validators**, it’s better to take a look at the **Custom Validators** in **argsv** [here...](https://github.com/mimseyedi/argsv/blob/master/src/argsv/_validators.py)

## 3.3. Callable Validators <a class="anchor" id="callable_validators"></a>
When defining a [Validation Pattern](https://github.com/mimseyedi/argsv/wiki/2.-Validation-Process#22-validation-pattern-), we can either use a **Validator** object as the **value** for a **key (argument name)**, or we can use a **callable** object, such as a **function** or **lambda**, as a **Validator**.

When we use the **second** method and define a **callable** object like a **function** or **lambda** as a **Validator**, it is **referred** to as a **Callable Validator**.

Here’s the translation you requested:

**argsv**, for greater **convenience** and to give more **flexibility** to the programmer, allows **callable** objects such as **functions** and **lambdas** to act as **Validators**. In fact, these **callable** objects are ultimately **converted** into a specific object called [CallVal](https://github.com/mimseyedi/argsv/blob/master/src/argsv/_validators.py#L414) or **Callable Validator**, but the **argsv** allows them to be received in [Validation Patterns](https://github.com/mimseyedi/argsv/wiki/2.-Validation-Process#22-validation-pattern-) as **functions** and **lambdas**."

However, an **important point** here is that we cannot consider just any **callable**, **function**, or **lambda** as a **Validator**! **Callable Validators** must follow a **rule**: just like other **Validators** and how the `__call__` dunder method is implemented for them, **Callable Validators** can only have **one parameter**. In simpler terms, they can only accept **one argument** (which is the argument to be validated).

```python
from argsv import argsval

@argsval(a=lambda x: x > 5)
def dummy(a):
    return a
```

Here, a **Callable Validator** is defined as a **lambda** function in the [Validation Pattern](https://github.com/mimseyedi/argsv/wiki/2.-Validation-Process#22-validation-pattern-) passed to the `argsval` **decorator**. It only accepts **one argument**, which is intended to be `a`!

The **important point** here is that **Callable Validators**, such as **functions** and **lambdas**, can return a **boolean** value. If their output is `False` (meaning the argument is not validated), `argsv` takes **responsibility** for generating the **error**. However, if necessary, these **Callable Validators** can also generate the error themselves.

```
ValidationError: Validation stopped while checking the argument passed to parameter 'a', in callable 'dummy'
From validator: <lambda>
 └── ValidationError: Validation failed due to return False from validator <function <lambda> at 0x1010edd00>
```

**Note:** If you're using **lambdas** as **Validators**, since the structure of lambdas doesn't allow raising exceptions directly, you can use the **built-in** and **pre-implemented** `callval` **Validator**. This allows you to specify the **type of error** and the **error message** you'd like to raise.

```python
from argsv import argsval
from argsv.validators import callval

@argsval(
    a=callval(
        lambda x: x > 5, 
        exc=ValueError, 
        exc_msg="'a' must be greater than 5!",
    )
)
def dummy(a):
    return a
```

In fact, **argsv** itself uses this **Validator** to convert **Callable Validators** into a formal **Validator** object!

## 3.4. Built-in Validators <a class="anchor" id="builtin-validators"></a>
**Built-in Validators** are a collection of **pre-implemented** and **ready-to-use** **Validators** designed to **simplify** and **accelerate** the validation process in **argsv**. 

These **Validators** **inherit** from the base abstract class [Validator](https://github.com/mimseyedi/argsv/blob/master/src/argsv/_validators.py#L72), adopting all the **features** of their parent class. 

To access **Built-in Validators**, you only need to **import** them from `argsv.validators`.

**For example**, there is a **Built-in Validator** named `typeval` that validates the **type** of arguments. Similar to the `isinstance` function, this Validator takes **a type**, a **tuple of types**, or a **union**, and checks the type of the argument against it.

```python
from argsv import argsval
from argsv.validators import typeval

@argsval(a=typeval(float))
def dummy(a):
    return a
```

Sometimes we need to perform **multiple validations** for a **single argument**! This can be achieved using the **Built-in Validator `multival`**. 

```python
from argsv import argsval
from argsv.validators import multival, typeval, fromto

@argsval(a=multival(typeval(float), fromto(1, 3)))
def dummy(a):
    return a
```

As you can see, this **Validator** allows **multiple validations** to be applied to a **single argument**. Here, the **type of the argument `a`** is validated using the **`typeval` Validator**, and the **range in which `a` can exist** is validated using the **`fromto` Validator**.

To explore the rest of the Built-in Validators and learn more about them, I recommend checking [here](https://github.com/mimseyedi/argsv/blob/master/src/argsv/validators.py). Nothing beats getting hands-on experience and experimenting. All the necessary docstrings and explanations about how the Built-in Validators work are available, so you can dive in and have a proper adventure yourself!