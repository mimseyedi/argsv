Hello! As the creator and primary developer of **argsv**, I’ve often felt that validating the arguments passed to a callable object directly within its body can be somewhat unpleasant. Personally, and perhaps for many others, I prefer the code within the body of a function to remain clean, focused, and directly related to its primary purpose. Including argument validation at the start of a function’s body doesn’t always look appealing and, at least for my perfectionist mind, lacks elegance.

Some might argue that in Python, argument validation isn’t always a necessity. In many cases, I agree with this perspective, as Python aims to accelerate implementation and development. However, there are certain scenarios—like when developing a module or library, or working on a specific project intended for use by others—where argument validation and generating precise errors become crucial. These practices help us act more responsibly when providing tools for others to use.

All these considerations led me to the idea of creating **argsv**. My primary goal was to separate the [validation process](https://github.com/mimseyedi/argsv/wiki/2.-Validation-Process) from the core logic of a function, making it simpler and more readable (hopefully, I’ve succeeded!).

To achieve this, I turned to **decorators** and designed a structure where argument validation could happen outside the body of the function. 

```python
from argsv import argsval

@argsval(b=lambda x: x != 0)
def div(a, b):
    return a / b
```

**For instance**, using the `argsval` **decorator** along with a lambda-based [Callable Validator](https://github.com/mimseyedi/argsv/wiki/3.-Validators#33-callable-validators-), I can define that the argument passed to parameter `b` must **not be zero**.

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
Here, using the `ArgsVal` **class**, the [validation process](https://github.com/mimseyedi/argsv/wiki/2.-Validation-Process) is performed within the function body. If the argument `b` is validated successfully, the rest of the function code will be executed.

**argsv** can be a simple and effective tool for validating the arguments of callables. It provides features that help implement the **validation process** in a more organized and straightforward way. In the following, some of the features and capabilities of **argsv** are highlighted.

### Features
- **Lightweight**: It doesn't rely on any external modules or libraries.  
- **Readable**: It separates the validation process from the main code, improving clarity.  
- **Simplifies Validation**: Makes the argument validation process easier.  
- **Precise Error Reporting**: Accurately displays errors in the validation process.  
- **Universal Compatibility**: Works with all types of callables.  
- **Custom Validators**: Allows you to implement your own customized validators.  
- **Built-in Validators**: Provides common and useful built-in validators.  
- **Extensible**: Designed to be flexible and expandable.

To understand how to use **argsv** and learn more, continue reading the documentation and move on to the next topic. In the following topics, the necessary concepts and features of **argsv** are covered, along with examples, and you can use them for reference.