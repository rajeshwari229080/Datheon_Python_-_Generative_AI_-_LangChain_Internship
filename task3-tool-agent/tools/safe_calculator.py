"""
Task 3: Multi-Tool Autonomous AI Agent
Tool 1: Restricted AST-Based Safe Math Calculator.
Strictly evaluates mathematical expressions using Python's Abstract Syntax Tree (AST).
Zero use of eval(), exec(), dunder introspection, or arbitrary system calls.
"""

from __future__ import annotations
import ast
import math
import operator
from typing import Any, Dict, Callable


class CalculatorSecurityError(Exception):
    """Raised when an expression attempts unsafe operations, imports, or dunder access."""
    pass


class SafeMathCalculator:
    """
    Safely computes mathematical expressions via recursive AST node evaluation.
    Guarantees isolation against code injection, memory corruption, and arbitrary execution.
    """

    ALLOWED_BINARY_OPS: Dict[type, Callable[[Any, Any], Any]] = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
    }

    ALLOWED_UNARY_OPS: Dict[type, Callable[[Any], Any]] = {
        ast.UAdd: operator.pos,
        ast.USub: operator.neg,
    }

    ALLOWED_FUNCTIONS: Dict[str, Callable[..., Any]] = {
        "sqrt": math.sqrt,
        "abs": abs,
        "round": round,
        "ceil": math.ceil,
        "floor": math.floor,
        "exp": math.exp,
        "log": math.log,
        "log10": math.log10,
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "min": min,
        "max": max,
        "pow": pow,
        "pi": math.pi,
        "e": math.e,
    }

    @classmethod
    def calculate(cls, expression: str) -> str:
        """
        Parses and evaluates a safe mathematical expression.
        Returns formatted result string or security/syntax error message.
        """
        expr_clean = expression.strip()
        if not expr_clean:
            return "Error: Empty expression."

        # Hard reject dangerous keyword patterns before AST parsing
        dangerous_keywords = ["__", "import", "exec", "eval", "globals", "locals", "builtins", "open", "os", "sys"]
        for kw in dangerous_keywords:
            if kw in expr_clean.lower():
                return f"Security Error: Forbidden token '{kw}' detected. Only pure mathematical expressions are allowed."

        try:
            tree = ast.parse(expr_clean, mode="eval")
            result = cls._eval_node(tree.body)
            # Format nicely
            if isinstance(result, float) and result.is_integer():
                return str(int(result))
            elif isinstance(result, float):
                return str(round(result, 6))
            return str(result)
        except ZeroDivisionError:
            return "Math Error: Division by zero is undefined."
        except CalculatorSecurityError as sec_err:
            return f"Security Error: {sec_err}"
        except Exception as e:
            return f"Syntax Error: Invalid mathematical expression ({e})."

    @classmethod
    def _eval_node(cls, node: ast.AST) -> Any:
        if isinstance(node, ast.Constant): # Numeric or constant literals
            if isinstance(node.value, (int, float)):
                return node.value
            raise CalculatorSecurityError(f"Constants of type {type(node.value)} are not permitted.")

        elif isinstance(node, ast.BinOp):
            left = cls._eval_node(node.left)
            right = cls._eval_node(node.right)
            op_type = type(node.op)
            if op_type in cls.ALLOWED_BINARY_OPS:
                # Guard against extreme powers causing CPU DOS
                if op_type is ast.Pow and (isinstance(right, (int, float)) and right > 1000):
                    raise CalculatorSecurityError("Exponent exceeds safety limit of 1000.")
                return cls.ALLOWED_BINARY_OPS[op_type](left, right)
            raise CalculatorSecurityError(f"Binary operator '{op_type.__name__}' is forbidden.")

        elif isinstance(node, ast.UnaryOp):
            operand = cls._eval_node(node.operand)
            op_type = type(node.op)
            if op_type in cls.ALLOWED_UNARY_OPS:
                return cls.ALLOWED_UNARY_OPS[op_type](operand)
            raise CalculatorSecurityError(f"Unary operator '{op_type.__name__}' is forbidden.")

        elif isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name):
                raise CalculatorSecurityError("Dynamic function dispatch is strictly forbidden.")
            func_name = node.func.id.lower()
            if func_name not in cls.ALLOWED_FUNCTIONS:
                raise CalculatorSecurityError(f"Function '{func_name}' is not in the safe mathematical whitelist.")

            func = cls.ALLOWED_FUNCTIONS[func_name]
            args = [cls._eval_node(arg) for arg in node.args]
            return func(*args)

        elif isinstance(node, ast.Name):
            # Allow math constants like pi and e
            name = node.id.lower()
            if name in ["pi", "e"]:
                return cls.ALLOWED_FUNCTIONS[name]
            raise CalculatorSecurityError(f"Variable reference '{node.id}' is forbidden.")

        else:
            raise CalculatorSecurityError(f"AST node type '{type(node).__name__}' is strictly forbidden.")
