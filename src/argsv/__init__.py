"""
@rgs✔

argsv is a library for validating arguments passed to callables.
With this library, you can validate arguments sent to callables
in a simpler, more readable, and well-defined context.

The goal of argsv development is to validate arguments outside
the body of callables, so that callables can be implemented more
readably and neatly, focusing on their main task.

argsv uses Validators, which are generally callables themselves
that can perform validation, to validate arguments.

Using decorators, argsv can, if necessary, take on the task of
validating the arguments of a callable outside the body of the callable,
and in a more readable way, it considers a specific space for
this so that it does not interfere with the main task of the callable!

Example::

    @argsval(a=validator_a, b=validator_b)
        def add(a, b):
            return a + b

However, argsv, by considering the ArgsVal class, also provides
the possibility to perform the argument validation process inside
the body of a function, so that those who are interested in validating
arguments inside the function body itself can do this.

Example::

    def add(a, b):
        # Validation section
        pattern = {a: validator_a, b: validator_b}
        av = ArgsVal(function, pattern, a, b)
        av.validate()
        # Function code section
        return a + b

By considering and implementing validators that are likely
to be used a lot, argsv also allows programmers to validate arguments
with ready-made validators and perform this process more quickly.
These validators are available in 'argsv.validators'

Github repo: https://github.com/mimseyedi/argsv
"""


from .validation import ArgsVal, argsval