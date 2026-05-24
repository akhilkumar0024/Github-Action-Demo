import pytest
from src.calculator import Calculator


@pytest.fixture
def calc():
    return Calculator()


def test_add(calc):
    assert calc.add(2, 3) == 5
    assert calc.add(-1, 1) == 0
    assert calc.add(-5, -5) == -10
    assert calc.add(1.5, 2.5) == 4.0


def test_subtract(calc):
    assert calc.subtract(10, 5) == 5
    assert calc.subtract(-1, -1) == 0
    assert calc.subtract(0, 5) == -5


def test_multiply(calc):
    assert calc.multiply(3, 4) == 12
    assert calc.multiply(-2, 3) == -6
    assert calc.multiply(0, 100) == 0
    assert calc.multiply(2.5, 2) == 5.0


def test_divide(calc):
    assert calc.divide(10, 2) == 5.0
    assert calc.divide(-6, 3) == -2.0
    assert calc.divide(5, 2) == 2.5


def test_divide_by_zero(calc):
    with pytest.raises(ValueError, match="Cannot divide by zero."):
        calc.divide(10, 0)


def test_power(calc):
    assert calc.power(2, 3) == 8
    assert calc.power(5, 0) == 1
    assert calc.power(4, 0.5) == 2.0


def test_square_root(calc):
    assert calc.square_root(9) == 3.0
    assert calc.square_root(0) == 0.0
    assert calc.square_root(2.25) == 1.5


def test_square_root_negative(calc):
    msg = "Cannot calculate square root of a negative number."
    with pytest.raises(ValueError, match=msg):
        calc.square_root(-4)
