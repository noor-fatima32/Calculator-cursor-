import pytest

from calculator.engine import CalculatorError, calculate, format_number


def test_addition_and_subtraction() -> None:
    assert calculate("2 + 3") == 5
    assert calculate("10 - 4") == 6


def test_operator_precedence() -> None:
    assert calculate("2 + 3 * 4") == 14
    assert calculate("(2 + 3) * 4") == 20


def test_division_and_decimals() -> None:
    assert calculate("10 / 4") == 2.5
    assert calculate("1.5 + 2.25") == 3.75


def test_unary_minus() -> None:
    assert calculate("-5 + 2") == -3
    assert calculate("-(2 + 3)") == -5


def test_division_by_zero() -> None:
    with pytest.raises(CalculatorError, match="zero"):
        calculate("8 / 0")


def test_invalid_expression() -> None:
    with pytest.raises(CalculatorError):
        calculate("2 +")
    with pytest.raises(CalculatorError):
        calculate("abc")


def test_format_whole_numbers() -> None:
    assert format_number(4.0) == "4"
    assert format_number(2.5) == "2.5"
