"""Simple desktop calculator window built with Tkinter."""

from __future__ import annotations

import tkinter as tk
from tkinter import font as tkfont

from calculator.engine import CalculatorError, calculate, format_number


_BG = "#1c1c1e"
_DISPLAY_BG = "#2c2c2e"
_KEY_BG = "#3a3a3c"
_OP_BG = "#ff9f0a"
_EQ_BG = "#30d158"
_FN_BG = "#636366"
_TEXT = "#f5f5f7"
_DISPLAY_TEXT = "#ffffff"
_ERROR = "#ff453a"


class CalculatorApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Calculator")
        self.root.configure(bg=_BG)
        self.root.minsize(320, 460)
        self.root.geometry("340x520")

        self.expression = ""
        self._just_evaluated = False

        self._build_layout()
        self.root.bind("<Key>", self._on_key)

    def _build_layout(self) -> None:
        pad = {"padx": 12, "pady": 12}
        display_frame = tk.Frame(self.root, bg=_BG)
        display_frame.pack(fill="x", **pad)

        self.display_var = tk.StringVar(value="0")
        display_font = tkfont.Font(family="Segoe UI", size=28, weight="bold")
        display = tk.Label(
            display_frame,
            textvariable=self.display_var,
            anchor="e",
            bg=_DISPLAY_BG,
            fg=_DISPLAY_TEXT,
            font=display_font,
            padx=16,
            pady=20,
        )
        display.pack(fill="x")

        grid = tk.Frame(self.root, bg=_BG)
        grid.pack(expand=True, fill="both", padx=12, pady=(0, 12))

        buttons = [
            ("C", self._clear, _FN_BG),
            ("⌫", self._backspace, _FN_BG),
            ("(", lambda: self._append("("), _FN_BG),
            (")", lambda: self._append(")"), _FN_BG),
            ("7", lambda: self._append("7"), _KEY_BG),
            ("8", lambda: self._append("8"), _KEY_BG),
            ("9", lambda: self._append("9"), _KEY_BG),
            ("÷", lambda: self._append("/"), _OP_BG),
            ("4", lambda: self._append("4"), _KEY_BG),
            ("5", lambda: self._append("5"), _KEY_BG),
            ("6", lambda: self._append("6"), _KEY_BG),
            ("×", lambda: self._append("*"), _OP_BG),
            ("1", lambda: self._append("1"), _KEY_BG),
            ("2", lambda: self._append("2"), _KEY_BG),
            ("3", lambda: self._append("3"), _KEY_BG),
            ("−", lambda: self._append("-"), _OP_BG),
            ("0", lambda: self._append("0"), _KEY_BG),
            (".", lambda: self._append("."), _KEY_BG),
            ("=", self._equals, _EQ_BG),
            ("+", lambda: self._append("+"), _OP_BG),
        ]

        for index, (label, command, color) in enumerate(buttons):
            row, column = divmod(index, 4)
            button = tk.Button(
                grid,
                text=label,
                command=command,
                bg=color,
                fg="#1c1c1e" if color in {_OP_BG, _EQ_BG} else _TEXT,
                activebackground=color,
                activeforeground="#1c1c1e" if color in {_OP_BG, _EQ_BG} else _TEXT,
                relief="flat",
                font=("Segoe UI", 16, "bold"),
                cursor="hand2",
            )
            button.grid(row=row, column=column, sticky="nsew", padx=4, pady=4, ipady=10)

        for i in range(5):
            grid.rowconfigure(i, weight=1)
        for i in range(4):
            grid.columnconfigure(i, weight=1)

    def _set_display(self, text: str, error: bool = False) -> None:
        self.display_var.set(text)
        # Color is applied on the label via the variable only; keep it simple.
        for child in self.root.winfo_children():
            if isinstance(child, tk.Frame):
                for widget in child.winfo_children():
                    if isinstance(widget, tk.Label):
                        widget.configure(fg=_ERROR if error else _DISPLAY_TEXT)

    def _append(self, char: str) -> None:
        if self._just_evaluated and (char.isdigit() or char == "."):
            self.expression = ""
        self._just_evaluated = False
        self.expression += char
        self._set_display(self.expression)

    def _clear(self) -> None:
        self.expression = ""
        self._just_evaluated = False
        self._set_display("0")

    def _backspace(self) -> None:
        if self._just_evaluated:
            self._clear()
            return
        self.expression = self.expression[:-1]
        self._set_display(self.expression or "0")

    def _equals(self) -> None:
        if not self.expression.strip():
            return
        try:
            result = format_number(calculate(self.expression))
        except CalculatorError as error:
            self._set_display(str(error), error=True)
            self._just_evaluated = True
            return
        self.expression = result
        self._just_evaluated = True
        self._set_display(result)

    def _on_key(self, event: tk.Event) -> None:
        key = event.keysym
        char = event.char

        if key in {"Return", "KP_Enter"}:
            self._equals()
        elif key in {"Escape", "Delete"}:
            self._clear()
        elif key == "BackSpace":
            self._backspace()
        elif char in "0123456789.+-*/()":
            self._append(char)


def run_gui() -> None:
    root = tk.Tk()
    CalculatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    run_gui()
