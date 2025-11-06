from collections.abc import Iterable
from numbers import Number
import math
from typing import Iterable as IterType, Any

def calculate_average(numbers: IterType[Any]) -> float:
    """Return the average of an iterable of numeric values.

    - Accepts any iterable (including generators).
    - Raises TypeError if `numbers` is None, a single numeric scalar, a string/bytes,
      or if any item is not convertible to float.
    - Raises ValueError for an empty iterable or if any item is non-finite (NaN/inf).
    - Uses Kahan summation for improved floating-point accuracy without building a list.
    """
    if numbers is None:
        raise TypeError("numbers must be an iterable of numeric values, got None")

    # reject a single numeric scalar (user probably meant to pass [x])
    if isinstance(numbers, Number):
        raise TypeError("numbers must be an iterable (e.g. list/tuple/generator), not a single number")

    # reject common accidental iterables that are not sequences of numbers
    if isinstance(numbers, (str, bytes)):
        raise TypeError("numbers must be an iterable of numeric values, not a string/bytes")

    it = iter(numbers)
    try:
        first = next(it)
    except StopIteration:
        raise ValueError("cannot calculate average of an empty sequence")

    # Kahan summation variables
    total = 0.0
    c = 0.0
    count = 0

    def _to_float(x):
        try:
            fx = float(x)
        except Exception:
            raise TypeError("all items must be numbers or convertible to float")
        if not math.isfinite(fx):
            raise ValueError("all items must be finite numbers (no NaN or infinity)")
        return fx

    # process first element and the rest
    for raw in (first, *it):
        fx = _to_float(raw)
        # Kahan summation step
        y = fx - c
        t = total + y
        c = (t - total) - y
        total = t
        count += 1

    return total / count

def add_numbers(x: int, y: int) -> int:
    """
    Adds two integers and returns their sum.

    Args:
        x (int): The first integer to add.
        y (int): The second integer to add.

    Returns:
        int: The sum of x and y.

    Raises:
        TypeError: If either x or y is not an integer.
    """
    if not isinstance(x, int) or not isinstance(y, int):
        raise TypeError("Both x and y must be integers.")
    return x + y