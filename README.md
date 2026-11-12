# Calculator

A small Python calculator for everyday arithmetic. It has a shared math engine, a command-line prompt, and a simple desktop window.

The app stays focused on the basics: addition, subtraction, multiplication, division, parentheses, and decimal numbers. Expressions are parsed directly, not passed to Python `eval()`.

## Features

- Four operations with standard precedence (`*` and `/` before `+` and `-`)
- Parentheses and negative numbers
- One-off command, interactive prompt, or windowed keypad
- Clear errors for invalid input and division by zero
- Standard library only (`tkinter` for the window)

## Requirements

- Python 3.10 or newer
- Tkinter (included with most Python installs on Windows)

## Run

From the project root:

```bash
# one expression
python -m calculator 2 + 3 * 4

# interactive prompt
python -m calculator

# desktop window
python -m calculator --gui
```

In the prompt, type `q` to quit.

## Tests

```bash
pip install -r requirements-dev.txt
python -m pytest
```

## Project layout

```text
calculator/     math engine, CLI, and GUI
tests/          unit tests for evaluation
```

## License

MIT
