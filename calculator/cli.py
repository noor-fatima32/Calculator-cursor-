"""Command-line interface for the calculator."""

from __future__ import annotations

import argparse
import sys

from calculator.engine import CalculatorError, calculate, format_number


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="calculator",
        description="A basic calculator. Pass an expression, start a prompt, or open the window.",
    )
    parser.add_argument(
        "expression",
        nargs="*",
        help="Expression to evaluate, for example: 2 + 3 * 4",
    )
    parser.add_argument(
        "--gui",
        action="store_true",
        help="Open the desktop calculator window.",
    )
    args = parser.parse_args(argv)

    if args.gui:
        from calculator.gui import run_gui

        run_gui()
        return 0

    if args.expression:
        return _print_result(" ".join(args.expression))

    return _repl()


def _print_result(expression: str) -> int:
    try:
        print(format_number(calculate(expression)))
        return 0
    except CalculatorError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1


def _repl() -> int:
    print("Basic Calculator  |  type an expression, or 'q' to quit")
    while True:
        try:
            line = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0

        if not line:
            continue
        if line.lower() in {"q", "quit", "exit"}:
            return 0

        try:
            print(format_number(calculate(line)))
        except CalculatorError as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    raise SystemExit(main())
