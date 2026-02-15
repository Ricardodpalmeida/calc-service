"""Decimal calculator engine - High precision calculations using Python decimal."""

from decimal import Decimal, getcontext, InvalidOperation
from typing import Optional
from enum import Enum


class CalculatorError(Exception):
    """Base exception for calculator errors."""
    code = "E5000"
    message = "Erro interno do servidor"
    field = None
    
    def __init__(self, details=None):
        self.details = details
        super().__init__(self.message)


class DivisionByZeroError(CalculatorError):
    """Raised when attempting division by zero."""
    code = "E4001"
    message = "Divisão por zero não permitida"
    field = "operand_b"


class NegativeSquareRootError(CalculatorError):
    """Raised when attempting square root of negative number."""
    code = "E4002"
    message = "Raiz quadrada de número negativo não permitida"
    field = "operand_a"


class InvalidInputError(CalculatorError):
    """Raised when input is invalid."""
    code = "E4005"
    message = "Operando inválido"
    field = None


class ExponentTooLargeError(CalculatorError):
    """Raised when exponent exceeds maximum allowed value."""
    code = "E4007"
    message = "Expoente excede limite de 1000"
    field = "operand_b"


class UnsupportedOperationError(CalculatorError):
    """Raised when operation is not supported."""
    code = "E4004"
    message = "Operação não suportada"
    field = "operation"


class Operation(Enum):
    """Supported mathematical operations."""
    ADD = "add"
    SUBTRACT = "subtract"
    MULTIPLY = "multiply"
    DIVIDE = "divide"
    MODULO = "modulo"
    POWER = "power"
    SQRT = "sqrt"


class CalculatorEngine:
    """
    High-precision decimal calculator engine.
    Uses Python's decimal module for arbitrary precision.
    ZERO FLOATING POINT OPERATIONS - All calculations use Decimal.
    """
    
    DEFAULT_PRECISION = 28
    MAX_PRECISION = 28
    MAX_EXPONENT = 1000
    
    def __init__(self, precision: int = DEFAULT_PRECISION):
        """Initialize calculator with specified precision."""
        self.precision = min(precision, self.MAX_PRECISION)
        getcontext().prec = self.precision
    
    def calculate(
        self,
        operation: Operation,
        operand_a: str,
        operand_b: Optional[str] = None
    ) -> Decimal:
        """
        Execute calculation with decimal precision.
        
        Args:
            operation: The operation to perform
            operand_a: First operand as string (preserves precision)
            operand_b: Second operand as string (optional for sqrt)
            
        Returns:
            Decimal result with configured precision
            
        Raises:
            DivisionByZeroError: If dividing by zero
            NegativeSquareRootError: If taking sqrt of negative number
            InvalidInputError: If operands are invalid
            ExponentTooLargeError: If exponent > 1000
            UnsupportedOperationError: If operation not supported
        """
        try:
            # Convert string to Decimal (NEVER from float!)
            a = Decimal(str(operand_a))
        except InvalidOperation as e:
            raise InvalidInputError(f"Operando A inválido: {operand_a}") from e
        
        # Square root only needs one operand
        if operation == Operation.SQRT:
            if a < 0:
                raise NegativeSquareRootError()
            return a.sqrt()
        
        # All other operations need two operands
        if operand_b is None:
            raise InvalidInputError("operand_b é obrigatório para esta operação")
        
        try:
            b = Decimal(str(operand_b))
        except InvalidOperation as e:
            raise InvalidInputError(f"Operando B inválido: {operand_b}") from e
        
        # Perform calculation
        if operation == Operation.ADD:
            return a + b
        
        elif operation == Operation.SUBTRACT:
            return a - b
        
        elif operation == Operation.MULTIPLY:
            return a * b
        
        elif operation == Operation.DIVIDE:
            if b == 0:
                raise DivisionByZeroError()
            return a / b
        
        elif operation == Operation.MODULO:
            if b == 0:
                raise DivisionByZeroError()
            return a % b
        
        elif operation == Operation.POWER:
            # Check exponent limit
            if abs(b) > self.MAX_EXPONENT:
                raise ExponentTooLargeError()
            return a ** int(b)
        
        else:
            raise UnsupportedOperationError()
    
    def set_precision(self, precision: int) -> None:
        """Update calculation precision."""
        self.precision = min(precision, self.MAX_PRECISION)
        getcontext().prec = self.precision
