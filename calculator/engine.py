"""Safe expression evaluation for a basic calculator.

Supports +, -, *, /, parentheses, decimals, and unary minus.
Does not use Python's eval().
"""

from __future__ import annotations

from dataclasses import dataclass


class CalculatorError(ValueError):
    """Raised when an expression cannot be evaluated."""


@dataclass
class _Token:
    kind: str
    value: str
    position: int


def calculate(expression: str) -> float:
    """Evaluate a basic arithmetic expression and return a float result."""
    tokens = _tokenize(expression)
    if not tokens:
        raise CalculatorError("Enter an expression.")
    parser = _Parser(tokens)
    result = parser.parse()
    if abs(result) == float("inf") or result != result:
        raise CalculatorError("Result is out of range.")
    return result


def format_number(value: float) -> str:
    """Format a result so whole numbers do not keep a trailing .0."""
    if value.is_integer():
        return str(int(value))
    return format(value, ".12g")


def _tokenize(expression: str) -> list[_Token]:
    tokens: list[_Token] = []
    i = 0
    length = len(expression)

    while i < length:
        char = expression[i]
        if char.isspace():
            i += 1
            continue

        if char.isdigit() or char == ".":
            start = i
            dot_count = 0
            while i < length and (expression[i].isdigit() or expression[i] == "."):
                if expression[i] == ".":
                    dot_count += 1
                    if dot_count > 1:
                        raise CalculatorError(f"Invalid number near position {start + 1}.")
                i += 1
            raw = expression[start:i]
            if raw == ".":
                raise CalculatorError(f"Invalid number near position {start + 1}.")
            tokens.append(_Token("NUMBER", raw, start))
            continue

        if char in "+-*/()":
            kind = "LPAREN" if char == "(" else "RPAREN" if char == ")" else "OP"
            tokens.append(_Token(kind, char, i))
            i += 1
            continue

        raise CalculatorError(f"Unexpected character '{char}' at position {i + 1}.")

    return tokens


class _Parser:
    def __init__(self, tokens: list[_Token]) -> None:
        self._tokens = tokens
        self._index = 0

    def parse(self) -> float:
        value = self._expression()
        if self._index < len(self._tokens):
            leftover = self._tokens[self._index]
            raise CalculatorError(f"Unexpected '{leftover.value}' at position {leftover.position + 1}.")
        return value

    def _expression(self) -> float:
        value = self._term()
        while self._match_op("+", "-"):
            op = self._previous().value
            right = self._term()
            value = value + right if op == "+" else value - right
        return value

    def _term(self) -> float:
        value = self._unary()
        while self._match_op("*", "/"):
            op = self._previous().value
            right = self._unary()
            if op == "/":
                if right == 0:
                    raise CalculatorError("Cannot divide by zero.")
                value = value / right
            else:
                value = value * right
        return value

    def _unary(self) -> float:
        if self._match_op("+", "-"):
            op = self._previous().value
            value = self._unary()
            return value if op == "+" else -value
        return self._primary()

    def _primary(self) -> float:
        token = self._peek()
        if token is None:
            raise CalculatorError("Expression is incomplete.")

        if token.kind == "NUMBER":
            self._advance()
            return float(token.value)

        if token.kind == "LPAREN":
            self._advance()
            value = self._expression()
            closing = self._peek()
            if closing is None or closing.kind != "RPAREN":
                raise CalculatorError("Missing closing parenthesis.")
            self._advance()
            return value

        raise CalculatorError(f"Unexpected '{token.value}' at position {token.position + 1}.")

    def _match_op(self, *operators: str) -> bool:
        token = self._peek()
        if token is not None and token.kind == "OP" and token.value in operators:
            self._advance()
            return True
        return False

    def _peek(self) -> _Token | None:
        if self._index >= len(self._tokens):
            return None
        return self._tokens[self._index]

    def _previous(self) -> _Token:
        return self._tokens[self._index - 1]

    def _advance(self) -> _Token:
        token = self._tokens[self._index]
        self._index += 1
        return token
