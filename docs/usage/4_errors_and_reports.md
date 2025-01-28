# 4. Errors and Reports
**argsv** employs its own **specific exceptions** to ensure that any errors generated are **precise**, **relevant**, and **informative**. By implementing specialized **exceptions**, **argsv** guarantees that developers receive clear and actionable feedback when something goes wrong.

Here, we will discuss the **various types** of **exceptions** used in **argsv** and provide comprehensive information about each one. This will help you understand their **purpose** and how to **handle** them effectively.

The **primary** and **foundational** exception implemented in **argsv** is [ArgsVError](#). This is **essentially** a **base exception** that **inherits** from Python's built-in `Exception`. It is primarily designed to serve as the **parent** class for all other exceptions, making the exception handling **structure** more **organized** and **systematic**.  

By referencing this exception, you are effectively addressing all potential errors that could be raised within **argsv**, as all other exceptions in the library—whether **directly** or **indirectly—inherit** from this base class, [ArgsVError](#).

## 4.1. PatternError <a class="anchor" id="pattern_error"></a>
The [PatternError](#) **exception** occurs **before** the [validation process](#) begins. When defining how a **validation process** should be executed using the [ArgsVal](#) **class** or the [argsval](#) **decorator**, if there is any **issue** with the **structure** of the [Validation Pattern](#), such as its **incompatibility** with the **callable** whose arguments are to be validated, or any other **structural mismatch**, a `PatternError` is raised.  

This **exception** provides a **precise error message** detailing the problem. Simply put, any **issue** or **error** related to the [Validation Pattern](#) is **reported** by the `PatternError` **exception**.

## 4.2. ValidatorError <a class="anchor" id="validator_error"></a>
The [ValidatorError](#) **exception** is raised by [validators](#) when an argument is **rejected**, and the **validation process** **fails**. Additionally, if a **validator** is not properly **initialized** or cannot start the [validation process](#), this **exception** is also **triggered**.  

In general, the `ValidatorError` covers any **issue** or **error** related to [validators](#), whether it's due to improper configuration or **failure** during the validation itself.

## 4.3. ValidationKeyError <a class="anchor" id="validation_key_error"></a>
The [ValidationKeyError](#) **exception** indicates an **issue** or **error** related to a [Validation Key](#). Since **Validation Keys** are a subset of [validators](#), `ValidationKeyError` **inherits** from the [ValidatorError](#) **exception**.

Whenever there is a **problem** in **defining** or **assigning** a [Validation Key](#), such as **incorrect configuration** or **invalid usage**, the `ValidationKeyError` **exception** is raised to **highlight** the **issue**.

## 4.4. ValidationError <a class="anchor" id="validation_error"></a>
The [ValidationError](#) exception is essentially the main error that a programmer encounters when working with `argsv`.  

In general, when the [validation process](#) is **executed** and **managed** by the [ArgsVal](#) **class** or the [argsval](#) **decorator**, any **exception** or **error** that occurs during the **validation process** is first **handled** internally. Subsequently, a `ValidationError` is **raised**.  

This **exception** not only points to the **location** where the issue occurred but also provides details about the **underlying error** that **caused** the [validation process](#) to **fail**. It acts as a **centralized mechanism** for delivering clear and actionable error messages related to **validation failures**.

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

Here, a [Callable Validator](#), customized using the [Built-in Validator](#) `callval`, specifies that `a` must be **greater than 5**. Otherwise, a `ValueError` with the **defined message** will be **raised**. If I call the `dummy` function and pass a number **less than 5** to the parameter `a`, I will encounter the following output:

```
ValidationError: Validation stopped while checking the argument passed to parameter 'a', in callable 'dummy'
From validator: <lambda>
 └── ValueError: 'a' must be greater than 5!
```

As you can see, a `ValidationError` **precisely** points to the **parameter** whose **validation** has **failed**, shows the **validator** that couldn't validate the parameter, and displays the error it produced.

<br>
<div style="display: flex; justify-content: space-between; text-align: center;">
  <a href="./previous.md">❮❮ Previous<br>(Validators)</a>
  <a href="./next.md">Next ❯❯<br>(Ways of Usage)</a>
</div>