import math
from typing import Union

Number = Union[int, float]


class Calculator:
    """A simple calculator application class."""

    def add(self, a: Number, b: Number) -> Number:
        """Return the sum of two numbers."""
        return a + b

    def subtract(self, a: Number, b: Number) -> Number:
        """Return the difference between two numbers."""
        return a - b

    def multiply(self, a: Number, b: Number) -> Number:
        """Return the product of two numbers."""
        return a * b

    def divide(self, a: Number, b: Number) -> float:
        """Return the division of a by b.
        Raises ValueError on zero division.
        """
        if b == 0:
            raise ValueError("Cannot divide by zero.")
        return float(a / b)

    def power(self, base: Number, exponent: Number) -> Number:
        """Return base raised to the power of exponent."""
        return base ** exponent

    def square_root(self, value: Number) -> float:
        """Return the square root of a value. Raises ValueError if negative."""
        if value < 0:
            raise ValueError(
                "Cannot calculate square root of a negative number."
            )
        return math.sqrt(value)


if __name__ == "__main__":
    calc = Calculator()
    print("Welcome to Simple Calculator!")
    print(f"5 + 3 = {calc.add(5, 3)}")
    print(f"10 - 4 = {calc.subtract(10, 4)}")
    print(f"3 * 6 = {calc.multiply(3, 6)}")
    print(f"8 / 2 = {calc.divide(8, 2)}")
    print(f"2^10 = {calc.power(2, 10)}")
    print(f"sqrt(16) = {calc.square_root(16)}")
