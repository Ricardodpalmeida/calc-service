"""Tests for calculator service."""

import pytest
from decimal import Decimal

from app.services.calculator import (
    CalculatorEngine,
    Operation,
    DivisionByZeroError,
    NegativeSquareRootError,
    InvalidInputError,
    ExponentTooLargeError
)


class TestCalculatorEngine:
    """Test suite for CalculatorEngine."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.calc = CalculatorEngine(precision=28)
    
    # === Addition Tests ===
    def test_addition_basic(self):
        """Test basic addition."""
        result = self.calc.calculate(Operation.ADD, "5", "3")
        assert result == Decimal("8")
    
    def test_addition_decimal_precision(self):
        """Test that 0.1 + 0.2 = 0.3 exactly (not 0.30000000000000004)."""
        result = self.calc.calculate(Operation.ADD, "0.1", "0.2")
        assert result == Decimal("0.3")
        assert str(result) == "0.3"
    
    def test_addition_negative(self):
        """Test addition with negative numbers."""
        result = self.calc.calculate(Operation.ADD, "-5", "3")
        assert result == Decimal("-2")
    
    def test_addition_large_numbers(self):
        """Test addition with large numbers."""
        result = self.calc.calculate(
            Operation.ADD, 
            "1234567890123456789012345678", 
            "8765432109876543210987654321"
        )
        assert result == Decimal("9999999999999999999999999999")
    
    # === Subtraction Tests ===
    def test_subtraction_basic(self):
        """Test basic subtraction."""
        result = self.calc.calculate(Operation.SUBTRACT, "10", "3")
        assert result == Decimal("7")
    
    def test_subtraction_decimal(self):
        """Test decimal subtraction."""
        result = self.calc.calculate(Operation.SUBTRACT, "1.5", "0.5")
        assert result == Decimal("1.0")
    
    # === Multiplication Tests ===
    def test_multiplication_basic(self):
        """Test basic multiplication."""
        result = self.calc.calculate(Operation.MULTIPLY, "4", "3")
        assert result == Decimal("12")
    
    def test_multiplication_decimal(self):
        """Test decimal multiplication."""
        result = self.calc.calculate(Operation.MULTIPLY, "0.5", "0.2")
        assert result == Decimal("0.1")
    
    # === Division Tests ===
    def test_division_basic(self):
        """Test basic division."""
        result = self.calc.calculate(Operation.DIVIDE, "10", "2")
        assert result == Decimal("5")
    
    def test_division_decimal_precision(self):
        """Test division maintains precision."""
        result = self.calc.calculate(Operation.DIVIDE, "10", "3")
        # Should have high precision (28 digits)
        assert len(str(result).replace(".", "").replace("-", "")) >= 28
    
    def test_division_by_zero(self):
        """Test division by zero raises error."""
        with pytest.raises(DivisionByZeroError) as exc_info:
            self.calc.calculate(Operation.DIVIDE, "10", "0")
        assert exc_info.value.code == "E4001"
        assert "zero" in exc_info.value.message.lower()
    
    # === Modulo Tests ===
    def test_modulo_basic(self):
        """Test basic modulo."""
        result = self.calc.calculate(Operation.MODULO, "10", "3")
        assert result == Decimal("1")
    
    def test_modulo_by_zero(self):
        """Test modulo by zero raises error."""
        with pytest.raises(DivisionByZeroError):
            self.calc.calculate(Operation.MODULO, "10", "0")
    
    # === Power Tests ===
    def test_power_basic(self):
        """Test basic power operation."""
        result = self.calc.calculate(Operation.POWER, "2", "3")
        assert result == Decimal("8")
    
    def test_power_zero(self):
        """Test power with zero exponent."""
        result = self.calc.calculate(Operation.POWER, "5", "0")
        assert result == Decimal("1")
    
    def test_power_negative_exponent(self):
        """Test power with negative exponent."""
        result = self.calc.calculate(Operation.POWER, "2", "-1")
        assert result == Decimal("0.5")
    
    def test_power_exponent_too_large(self):
        """Test power with exponent > 1000 raises error."""
        with pytest.raises(ExponentTooLargeError) as exc_info:
            self.calc.calculate(Operation.POWER, "2", "1001")
        assert exc_info.value.code == "E4007"
    
    # === Square Root Tests ===
    def test_sqrt_basic(self):
        """Test basic square root."""
        result = self.calc.calculate(Operation.SQRT, "16")
        assert result == Decimal("4")
    
    def test_sqrt_decimal(self):
        """Test square root of decimal."""
        result = self.calc.calculate(Operation.SQRT, "2")
        # sqrt(2) should have high precision
        assert len(str(result).replace(".", "")) >= 28
    
    def test_sqrt_zero(self):
        """Test square root of zero."""
        result = self.calc.calculate(Operation.SQRT, "0")
        assert result == Decimal("0")
    
    def test_sqrt_negative(self):
        """Test square root of negative raises error."""
        with pytest.raises(NegativeSquareRootError) as exc_info:
            self.calc.calculate(Operation.SQRT, "-4")
        assert exc_info.value.code == "E4002"
    
    def test_sqrt_requires_only_one_operand(self):
        """Test sqrt works with only operand_a."""
        result = self.calc.calculate(Operation.SQRT, "25")
        assert result == Decimal("5")
    
    # === Error Handling Tests ===
    def test_missing_operand_b_for_addition(self):
        """Test that operand_b is required for addition."""
        with pytest.raises(InvalidInputError):
            self.calc.calculate(Operation.ADD, "5", None)
    
    def test_invalid_operand_a(self):
        """Test invalid operand_a raises error."""
        with pytest.raises(InvalidInputError):
            self.calc.calculate(Operation.ADD, "abc", "5")
    
    def test_invalid_operand_b(self):
        """Test invalid operand_b raises error."""
        with pytest.raises(InvalidInputError):
            self.calc.calculate(Operation.ADD, "5", "xyz")
    
    # === Precision Tests ===
    def test_precision_setting(self):
        """Test precision can be changed."""
        calc_low = CalculatorEngine(precision=5)
        calc_low.set_precision(5)
        result = calc_low.calculate(Operation.DIVIDE, "1", "3")
        # With precision 5, should have fewer digits
        str_result = str(result)
        # Just verify it works with different precision
        assert "0.3333" in str_result
    
    def test_max_precision_enforced(self):
        """Test that precision cannot exceed 28."""
        calc = CalculatorEngine(precision=50)
        assert calc.precision == 28


class TestDecimalPrecision:
    """Test suite specifically for decimal precision guarantees."""
    
    def test_floating_point_problem(self):
        """Demonstrate the floating-point problem we avoid."""
        # This is what happens with floats
        float_result = 0.1 + 0.2
        assert float_result != 0.3  # Float problem!
        
        # This is what we guarantee with Decimal
        calc = CalculatorEngine()
        decimal_result = calc.calculate(Operation.ADD, "0.1", "0.2")
        assert decimal_result == Decimal("0.3")  # Exact!
    
    def test_decimal_string_input(self):
        """Test that string inputs preserve precision."""
        calc = CalculatorEngine()
        # Large decimal that would lose precision as float
        large_decimal = "0.1234567890123456789012345678"
        result = calc.calculate(Operation.ADD, large_decimal, "0")
        assert str(result) == large_decimal
