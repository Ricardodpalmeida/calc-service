#!/usr/bin/env python3
"""Calc Service CLI - Command line interface for high-precision calculations."""

import argparse
import json
import sys
from decimal import Decimal, InvalidOperation
from typing import Optional

# Add backend to path
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.services.calculator import CalculatorEngine, Operation
from app.services.calculator import (
    DivisionByZeroError,
    InvalidInputError,
    UnsupportedOperationError
)


def parse_operation(op: str) -> Operation:
    """Parse operation string to Operation enum."""
    mapping = {
        'add': Operation.ADD,
        '+': Operation.ADD,
        'subtract': Operation.SUBTRACT,
        '-': Operation.SUBTRACT,
        'multiply': Operation.MULTIPLY,
        '*': Operation.MULTIPLY,
        'divide': Operation.DIVIDE,
        '/': Operation.DIVIDE,
        'modulo': Operation.MODULO,
        '%': Operation.MODULO,
        'power': Operation.POWER,
        '^': Operation.POWER,
        'sqrt': Operation.SQRT,
        '√': Operation.SQRT,
    }
    
    op_lower = op.lower().strip()
    if op_lower not in mapping:
        raise UnsupportedOperationError()
    return mapping[op_lower]


def calculate(operation: str, a: str, b: Optional[str] = None, json_output: bool = False):
    """Execute calculation and output result."""
    try:
        calc = CalculatorEngine()
        op = parse_operation(operation)
        
        result = calc.calculate(op, a, b)
        
        if json_output:
            output = {
                "result": str(result),
                "operation": operation,
                "a": a,
                "b": b,
                "success": True
            }
            print(json.dumps(output))
        else:
            print(result)
            
    except DivisionByZeroError:
        error_msg = "Error: Division by zero"
        if json_output:
            print(json.dumps({"error": error_msg, "code": "DIVISION_BY_ZERO", "success": False}))
        else:
            print(error_msg, file=sys.stderr)
        sys.exit(1)
        
    except InvalidInputError as e:
        error_msg = f"Error: Invalid input - {e.message}"
        if json_output:
            print(json.dumps({"error": error_msg, "code": "INVALID_INPUT", "success": False}))
        else:
            print(error_msg, file=sys.stderr)
        sys.exit(1)
        
    except UnsupportedOperationError:
        error_msg = f"Error: Unsupported operation '{operation}'"
        if json_output:
            print(json.dumps({"error": error_msg, "code": "UNSUPPORTED_OPERATION", "success": False}))
        else:
            print(error_msg, file=sys.stderr)
        sys.exit(1)


def list_operations():
    """List all available operations."""
    operations = [
        ("add", "+", "Addition"),
        ("subtract", "-", "Subtraction"),
        ("multiply", "*", "Multiplication"),
        ("divide", "/", "Division"),
        ("modulo", "%", "Modulo"),
        ("power", "^", "Power"),
        ("sqrt", "√", "Square Root (single operand)"),
    ]
    
    print("Available operations:")
    for name, symbol, desc in operations:
        print(f"  {name:10} ({symbol:3}) - {desc}")


def main():
    parser = argparse.ArgumentParser(
        description="High-precision decimal calculator for agents",
        prog="calc-service"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Calculate command
    calc_parser = subparsers.add_parser("calculate", aliases=["calc"], help="Perform calculation")
    calc_parser.add_argument("--operation", "-o", required=True, help="Operation (add, subtract, multiply, divide, modulo, power, sqrt)")
    calc_parser.add_argument("--a", required=True, help="First operand")
    calc_parser.add_argument("--b", help="Second operand (optional for sqrt)")
    calc_parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")
    
    # List operations command
    list_parser = subparsers.add_parser("operations", aliases=["ops", "list"], help="List available operations")
    
    args = parser.parse_args()
    
    if args.command in ("calculate", "calc"):
        calculate(args.operation, args.a, args.b, args.json)
    elif args.command in ("operations", "ops", "list"):
        list_operations()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()