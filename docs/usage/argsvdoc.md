![](https://raw.githubusercontent.com/mimseyedi/argsv/master/docs/images/argsv-poster.png)

**argsv** is a library for validating arguments passed to callables. With this library, you can validate arguments sent to callables in a **simpler**, more **readable**, and **well-defined** context.

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

* [1. Why **argsv**?](#why_argsv)
* [2. Validation Process](#validation_process)
  * [2.1. Internal Validation](#internal_validation)
  * [2.2. Validation Pattern](#validation_pattern)
  * [2.3. Validation by Decorator](#validation_by_decorator)
* [3. Validators](#validators)
  * [3.1. Basic Validator](#basic_validator)
    * [3.1.1. Validation Key](#validation_key)
  * [3.2. Custom Validators](#custom_validators)
  * [3.3. Callable Validators](#callable_validators)
  * [3.4. Built-in Validators](#builtin_validators)
* [4. Errors and Reports](#errors_and_reports)
  * [4.1. PatternError](#pattern_error)
  * [4.2. ValidatorError](#pattern_error)
  * [4.3. ValidationKeyError](#validation_key_error)
  * [4.4. ValidationError](#pattern_error)
* [5. Ways of Usage](#ways_of_usage)
* [6. Contribution](#contribution)