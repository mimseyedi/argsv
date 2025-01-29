The **validation process** in **argsv** is straightforward and follows a well-defined structure. It examines and validates arguments according to a specific **pattern**. If the arguments **fail** validation, the relevant **error** is precisely generated; **otherwise**, the **callable** with **validated arguments** proceeds to **execution**. Essentially, **argsv** functions like a **checkpoint gate—only** allowing the **callable** to **execute** if its arguments **successfully** pass through the gate.

There are **two** methods for creating the argument **validation process** for callables using **argsv**:

**1. Internal Validation:**
- Using the `ArgsVal` **class**
- Using [Built-in Validators](https://github.com/mimseyedi/argsv/wiki/3.-Validators#34-built-in-validators-)

**2. External Validation:**
- Validation via the `argsval` **Decorator**

## 2.1. Internal Validation <a class="anchor" id="internal_validation"></a>
**argsv** delegates the responsibility of creating and managing argument validation for callables to the `ArgsVal` **class**. This class takes a callable along with its arguments and a [Validation Pattern](https://github.com/mimseyedi/argsv/wiki/2.-Validation-Process#22-validation-pattern-) to construct an object. By calling its `validate` method, the **validation process** is performed.

The method of validating arguments in `ArgsVal` works as follows: it accepts a **callable** with its **arguments** and **matches** them against the provided **Validation Pattern**. If this process is successful, the arguments are **validated**, and the callable can proceed with its operation. Otherwise, program execution is halted, raising a [ValidationError](https://github.com/mimseyedi/argsv/wiki/4.-Errors-and-Reports#44-validationerror-) **exception**, and a related message is displayed.

**For example**, you can import `ArgsVal` and perform this process within the body of a **function** as follows:

```python
from argsv import ArgsVal

def div(a, b):
    # Validation section
    ArgsVal(
        div, {'b': lambda x: x != 0}, a, b
    ).validate()
    # Function code
    return a / b
```

Here, by passing the function `div` along with its arguments (`a` and `b`) and a [Validation Pattern](#https://github.com/mimseyedi/argsv/wiki/2.-Validation-Process#22-validation-pattern-) in the form of a dictionary to `ArgsVal`, we used a **lambda** function to specify that the value of `b` must not be **equal to zero**!

## 2.2. Validation Pattern <a class="anchor" id="validation_pattern"></a>
The **Validation Pattern** is a **blueprint** that defines how arguments should be structured! Essentially, it specifies the conditions an argument must meet to be **validated**. This process is implemented using a **dictionary**, where the **keys** represent the names of the arguments (or more specifically, the names of the parameters to which the arguments are passed), and the **values** are [Validators](https://github.com/mimseyedi/argsv/wiki/3.-Validators) responsible for **validating** the arguments and determining whether they are **accepted** or **rejected**. 

In essence, the **Validation Pattern** acts as a **dictionary** that connects the arguments to the [Validators](https://github.com/mimseyedi/argsv/wiki/3.-Validators), ensuring the arguments meet the specified validation criteria.

```python
{'a': validator_a, 'b': validator_b}
```

When you pass a dictionary as the **Validation Pattern** to the `ArgsVal` **class**, an object named [Pattern](https://github.com/mimseyedi/argsv/blob/master/src/argsv/_pattern.py#L43) is created. This object are structured to consistently manage **validation patterns** and can perform tasks such as:  
- Returning the **validators** associated with a specific argument 
- Verifying the compatibility of the **pattern** with a **callable** object  
- And ... 

You can access this object by referring to the `pattern` attribute:

```
>>> av = ArgsVal(div, {'b': lambda x: x != 0}, a, b)
>>> av.pattern
ValidationPattern({'b': CallableValidator(<function <lambda> at 0x10253fce0>)})
```

Here, as you can see, there is a `ValidationPattern` object whose **initial pattern** is visible in the form of a **dictionary**, and the **lambda** function responsible for validation has now been **converted** into an object called [CallableValidator](https://github.com/mimseyedi/argsv/wiki/3.-Validators#33-callable-validators-), which is considered an **official** and **recognized** **Validator** for **argsv**. 

More detailed information can be found in the section about [Validators](https://github.com/mimseyedi/argsv/wiki/3.-Validators).

## 2.3. Validation by Decorator <a class="anchor" id="validation_by_decorator"></a>

To validate the arguments of callables, it is possible to perform the **validation process** outside the function body in the form of a **decorator**. By importing the `argsval` **decorator**, we can validate the arguments of a callable simply by passing a [Validation Pattern](https://github.com/mimseyedi/argsv/wiki/2.-Validation-Process#22-validation-pattern-) as keyword arguments.

The `argsval` **decorator** is simply a **readable** and **fast** interface for the `ArgsVal` **class**. In fact, the `argsval` **decorator** uses the `ArgsVal` **class** to create an object for **executing** and **managing** the **validation process** without adding any extra functionality. The advantage of the `argsval` **decorator** is its **beauty** and **readability** in usage, along with **faster** implementation of validation operations, which can be used in a **separate** section, apart from the body of the callable.

```python
from argsv import argsval

@argsval(b=lambda x: x != 0)
def div(a, b):
    return a/ b
```
Here, the `argsval` **decorator**, by receiving **keyword arguments** as the [Validation Pattern](https://github.com/mimseyedi/argsv/wiki/2.-Validation-Process#22-validation-pattern-), validates the argument `b` using a **lambda** function. Its placement above the `div` function clearly demonstrates this process and enhances readability.

In the next topic, [Validators](https://github.com/mimseyedi/argsv/wiki/3.-Validators) are discussed in detail. If you need more information about them, you can refer to the next topic.