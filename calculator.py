"""Calculator module with basic arithmetic operations."""


def _validate_inputs(*args: object) -> None:
    """Validate that all inputs are numeric types.

    Args:
        *args: Values to validate.

    Raises:
        TypeError: If any argument is not int or float.
    """
    for value in args:
        if not isinstance(value, (int, float)):
            raise TypeError(f"Expected numeric type, got {type(value).__name__}")


def add(a: float, b: float) -> float:
    """Return the sum of two numbers.

    Args:
        a: First number.
        b: Second number.

    Returns:
        Sum of a and b.
    """
    _validate_inputs(a, b)
    return a + b


def subtract(a: float, b: float) -> float:
    """Return the difference of two numbers.

    Args:
        a: First number.
        b: Second number.

    Returns:
        Result of a minus b.
    """
    _validate_inputs(a, b)
    return a - b


def multiply(a: float, b: float) -> float:
    """Return the product of two numbers.

    Args:
        a: First number.
        b: Second number.

    Returns:
        Product of a and b.
    """
    _validate_inputs(a, b)
    return a * b


def divide(a: float, b: float) -> float:
    """Return the quotient of two numbers.

    Args:
        a: Numerator.
        b: Denominator.

    Returns:
        Result of a divided by b.

    Raises:
        ZeroDivisionError: If b is zero.
    """
    _validate_inputs(a, b)
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b
