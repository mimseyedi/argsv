**argsv** employs its own **specific exceptions** to ensure that any errors generated are **precise**, **relevant**, and **informative**. By implementing specialized **exceptions**, **argsv** guarantees that developers receive clear and actionable feedback when something goes wrong.

Here, we will discuss the **various types** of **exceptions** used in **argsv** and provide comprehensive information about each one. This will help you understand their **purpose** and how to **handle** them effectively.

The **primary** and **foundational** exception implemented in **argsv** is [ArgsVError](https://github.com/mimseyedi/argsv/blob/master/src/argsv/errors.py#L10). This is **essentially** a **base exception** that **inherits** from Python's built-in `Exception`. It is primarily designed to serve as the **parent** class for all other exceptions, making the exception handling **structure** more **organized** and **systematic**.  

By referencing this exception, you are effectively addressing all potential errors that could be raised within **argsv**, as all other exceptions in the library—whether **directly** or **indirectly—inherit** from this base class, [ArgsVError](https://github.com/mimseyedi/argsv/blob/master/src/argsv/errors.py#L10).

## 4.1. PatternError <a class="anchor" id="pattern_error"></a>
The [PatternError](https://github.com/mimseyedi/argsv/blob/master/src/argsv/errors.py#L37) **exception** occurs **before** the [validation process](https://github.com/mimseyedi/argsv/wiki/2.-Validation-Process) begins. When defining how a **validation process** should be executed using the [ArgsVal](https://github.com/mimseyedi/argsv/wiki/2.-Validation-Process#21-internal-validation-) **class** or the [argsval](https://github.com/mimseyedi/argsv/wiki/2.-Validation-Process#23-validation-by-decorator-) **decorator**, if there is any **issue** with the **structure** of the [Validation Pattern](https://github.com/mimseyedi/argsv/wiki/2.-Validation-Process#22-validation-pattern-), such as its **incompatibility** with the **callable** whose arguments are to be validated, or any other **structural mismatch**, a `PatternError` is raised.  

This **exception** provides a **precise error message** detailing the problem. Simply put, any **issue** or **error** related to the [Validation Pattern](https://github.com/mimseyedi/argsv/wiki/2.-Validation-Process#22-validation-pattern-) is **reported** by the `PatternError` **exception**.

## 4.2. ValidatorError <a class="anchor" id="validator_error"></a>
The [ValidatorError](https://github.com/mimseyedi/argsv/blob/master/src/argsv/errors.py#L23) **exception** is raised by [validators](https://github.com/mimseyedi/argsv/wiki/3.-Validators) when an argument is **rejected**, and the **validation process** **fails**. Additionally, if a **validator** is not properly **initialized** or cannot start the [validation process](https://github.com/mimseyedi/argsv/wiki/2.-Validation-Process), this **exception** is also **triggered**.  

In general, the `ValidatorError` covers any **issue** or **error** related to [validators](https://github.com/mimseyedi/argsv/wiki/3.-Validators), whether it's due to improper configuration or **failure** during the validation itself.

## 4.3. ValidationKeyError <a class="anchor" id="validation_key_error"></a>
The [ValidationKeyError](https://github.com/mimseyedi/argsv/blob/master/src/argsv/errors.py#L30) **exception** indicates an **issue** or **error** related to a [Validation Key](https://github.com/mimseyedi/argsv/wiki/3.-Validators#311-validation-key-). Since **Validation Keys** are a subset of [validators](https://github.com/mimseyedi/argsv/wiki/3.-Validators), `ValidationKeyError` **inherits** from the [ValidatorError](https://github.com/mimseyedi/argsv/blob/master/src/argsv/errors.py#L23) **exception**.

Whenever there is a **problem** in **defining** or **assigning** a [Validation Key](https://github.com/mimseyedi/argsv/wiki/3.-Validators#311-validation-key-), such as **incorrect configuration** or **invalid usage**, the `ValidationKeyError` **exception** is raised to **highlight** the **issue**.

## 4.4. ValidationError <a class="anchor" id="validation_error"></a>
The [ValidationError](https://github.com/mimseyedi/argsv/blob/master/src/argsv/errors.py#L17) exception is essentially the main error that a programmer encounters when working with **argsv**.  

In general, when the [validation process](https://github.com/mimseyedi/argsv/wiki/2.-Validation-Process) is **executed** and **managed** by the [ArgsVal](https://github.com/mimseyedi/argsv/wiki/2.-Validation-Process#21-internal-validation-) **class** or the [argsval](https://github.com/mimseyedi/argsv/wiki/2.-Validation-Process#23-validation-by-decorator-) **decorator**, any **exception** or **error** that occurs during the **validation process** is first **handled** internally. Subsequently, a `ValidationError` is **raised**.  

This **exception** not only points to the **location** where the issue occurred but also provides details about the **underlying error** that **caused** the [validation process](https://github.com/mimseyedi/argsv/wiki/2.-Validation-Process) to **fail**. It acts as a **centralized mechanism** for delivering clear and actionable error messages related to **validation failures**.

**For example**, consider the following code:

```python
from argsv import argsval
from argsv.validators import callval

@argsval(
    a=callval(
        lambda x: x > 5, 
        exc=ValueError, 
        exc_msg="'a' must be greater than 5!",
    ),
)
def dummy(a):
    return a
```

Here, a [Callable Validator](https://github.com/mimseyedi/argsv/wiki/3.-Validators#33-callable-validators-), customized using the [Built-in Validator](https://github.com/mimseyedi/argsv/wiki/3.-Validators#34-built-in-validators-) `callval`, specifies that `a` must be **greater than 5**. Otherwise, a `ValueError` with the **defined message** will be **raised**. If I call the `dummy` function and pass a number **less than 5** to the parameter `a`, I will encounter the following output:

```
ValidationError: Validation stopped while checking the argument passed to parameter 'a', in callable 'dummy'
From validator: <lambda>
 └── ValueError: 'a' must be greater than 5!
```

As you can see, a `ValidationError` **precisely** points to the **parameter** whose **validation** has **failed**, shows the **validator** that couldn't validate the parameter, and displays the error it produced.