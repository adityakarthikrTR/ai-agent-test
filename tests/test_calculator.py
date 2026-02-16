"""Comprehensive tests for the calculator module."""

import pytest

from calculator import add, subtract, multiply, divide


# =============================================================================
# Level 1: Unit Tests — Happy Path
# =============================================================================


class TestAdd:
    """Unit tests for the add function."""

    def test_add_positive_numbers(self):
        assert add(2, 3) == 5

    def test_add_negative_numbers(self):
        assert add(-2, -3) == -5

    def test_add_mixed_signs(self):
        assert add(-2, 3) == 1

    def test_add_floats(self):
        assert add(1.5, 2.5) == 4.0

    def test_add_zero(self):
        assert add(0, 5) == 5

    def test_add_both_zero(self):
        assert add(0, 0) == 0


class TestSubtract:
    """Unit tests for the subtract function."""

    def test_subtract_positive_numbers(self):
        assert subtract(5, 3) == 2

    def test_subtract_negative_result(self):
        assert subtract(3, 5) == -2

    def test_subtract_negative_numbers(self):
        assert subtract(-5, -3) == -2

    def test_subtract_floats(self):
        assert subtract(5.5, 2.5) == 3.0

    def test_subtract_zero(self):
        assert subtract(5, 0) == 5

    def test_subtract_from_zero(self):
        assert subtract(0, 5) == -5


class TestMultiply:
    """Unit tests for the multiply function."""

    def test_multiply_positive_numbers(self):
        assert multiply(3, 4) == 12

    def test_multiply_negative_numbers(self):
        assert multiply(-3, -4) == 12

    def test_multiply_mixed_signs(self):
        assert multiply(-3, 4) == -12

    def test_multiply_by_zero(self):
        assert multiply(5, 0) == 0

    def test_multiply_by_one(self):
        assert multiply(5, 1) == 5

    def test_multiply_floats(self):
        assert multiply(2.5, 4.0) == 10.0


class TestDivide:
    """Unit tests for the divide function."""

    def test_divide_positive_numbers(self):
        assert divide(10, 2) == 5.0

    def test_divide_negative_numbers(self):
        assert divide(-10, -2) == 5.0

    def test_divide_mixed_signs(self):
        assert divide(-10, 2) == -5.0

    def test_divide_floats(self):
        assert divide(7.5, 2.5) == 3.0

    def test_divide_result_is_float(self):
        assert divide(7, 2) == 3.5

    def test_divide_by_one(self):
        assert divide(5, 1) == 5.0

    def test_divide_zero_numerator(self):
        assert divide(0, 5) == 0.0


# =============================================================================
# Level 1: Unit Tests — Edge Cases (parametrized)
# =============================================================================


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (1e15, 1e15, 2e15),
        (-1e15, 1e15, 0),
        (0.1 + 0.2, 0, pytest.approx(0.3)),
        (999999999, 1, 1000000000),
    ],
)
def test_add_edge_cases(a, b, expected):
    """Test add with large numbers and floating point precision."""
    assert add(a, b) == expected


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (1e15, 1e15, 0),
        (0.3, 0.1, pytest.approx(0.2)),
    ],
)
def test_subtract_edge_cases(a, b, expected):
    """Test subtract with large numbers and floating point precision."""
    assert subtract(a, b) == expected


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (1e10, 1e10, 1e20),
        (0.1, 0.1, pytest.approx(0.01)),
        (-1, -1, 1),
    ],
)
def test_multiply_edge_cases(a, b, expected):
    """Test multiply with large numbers and floating point precision."""
    assert multiply(a, b) == expected


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (1e15, 1, 1e15),
        (1, 3, pytest.approx(0.3333333333)),
        (-1, -1, 1.0),
    ],
)
def test_divide_edge_cases(a, b, expected):
    """Test divide with large numbers and floating point precision."""
    assert divide(a, b) == expected


# =============================================================================
# Level 1: Unit Tests — Error Cases
# =============================================================================


class TestDivideByZero:
    """Test division by zero handling."""

    def test_divide_by_zero_raises(self):
        with pytest.raises(ZeroDivisionError, match="Cannot divide by zero"):
            divide(10, 0)

    def test_divide_by_zero_float(self):
        with pytest.raises(ZeroDivisionError, match="Cannot divide by zero"):
            divide(10.5, 0)

    def test_divide_by_zero_both_zero(self):
        with pytest.raises(ZeroDivisionError, match="Cannot divide by zero"):
            divide(0, 0)


class TestInvalidInputTypes:
    """Test that non-numeric inputs raise TypeError."""

    @pytest.mark.parametrize("func", [add, subtract, multiply, divide])
    def test_string_input(self, func):
        with pytest.raises(TypeError, match="Expected numeric type"):
            func("a", 1)

    @pytest.mark.parametrize("func", [add, subtract, multiply, divide])
    def test_none_input(self, func):
        with pytest.raises(TypeError, match="Expected numeric type"):
            func(None, 1)

    @pytest.mark.parametrize("func", [add, subtract, multiply, divide])
    def test_list_input(self, func):
        with pytest.raises(TypeError, match="Expected numeric type"):
            func([1], 1)

    @pytest.mark.parametrize("func", [add, subtract, multiply, divide])
    def test_bool_second_arg(self, func):
        with pytest.raises(TypeError, match="Expected numeric type"):
            func(1, "b")


# =============================================================================
# Level 3: Functional Tests — Calculator Workflows
# =============================================================================


class TestCalculatorWorkflows:
    """Test realistic calculator usage scenarios."""

    def test_chained_operations(self):
        """Simulate: (5 + 3) * 2 - 4 / 2 = 14"""
        result = add(5, 3)
        result = multiply(result, 2)
        result = subtract(result, divide(4, 2))
        assert result == 14.0

    def test_percentage_calculation(self):
        """Calculate 15% of 200: 200 * 15 / 100 = 30"""
        result = divide(multiply(200, 15), 100)
        assert result == 30.0

    def test_average_calculation(self):
        """Average of 10, 20, 30: (10 + 20 + 30) / 3 = 20"""
        total = add(add(10, 20), 30)
        result = divide(total, 3)
        assert result == 20.0

    def test_temperature_conversion(self):
        """Convert 100°C to °F: (100 * 9/5) + 32 = 212"""
        result = add(multiply(100, divide(9, 5)), 32)
        assert result == 212.0


# =============================================================================
# Level 4: Edge & Security Tests
# =============================================================================


class TestLargeInputs:
    """Test with very large numbers to check overflow handling."""

    def test_add_very_large(self):
        result = add(1e308, 1e308)
        assert result == float("inf")

    def test_multiply_very_large(self):
        result = multiply(1e200, 1e200)
        assert result == float("inf")

    def test_subtract_very_large(self):
        result = subtract(1e308, 1e308)
        assert result == 0.0

    def test_divide_very_small_denominator(self):
        result = divide(1, 1e-308)
        assert result == 1e308
