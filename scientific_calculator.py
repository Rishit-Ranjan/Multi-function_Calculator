import tkinter as tk
import math
from tkinter import simpledialog

class ScientificCalculator:
    def __init__(self, master, history=None, settings=None):
        self.master = master
        self.history = history
        self.settings = settings or {}
        master.configure(bg="#f7f7f7")
        
        # Configure grid for responsiveness
        master.grid_rowconfigure(0, weight=0)  # Entry
        master.grid_rowconfigure(1, weight=1)  # Buttons space
        for i in range(4):
            master.grid_columnconfigure(i, weight=1)

        self.entry = tk.Entry(master, font=("Arial", 16), justify="right", bd=0, bg="#e6e8ec")
        self.entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="we", ipady=12)

        btns = [
            ("sin", 1, 0), ("cos", 1, 1), ("tan", 1, 2), ("sqrt", 1, 3),
            ("ln", 2, 0), ("log", 2, 1), ("!", 2, 2), ("x^y", 2, 3),
            ("7", 3, 0), ("8", 3, 1), ("9", 3, 2), ("(", 3, 3),
            ("4", 4, 0), ("5", 4, 1), ("6", 4, 2), (")", 4, 3),
            ("1", 5, 0), ("2", 5, 1), ("3", 5, 2), ("^", 5, 3),
            ("0", 6, 0), (".", 6, 1), ("AC", 6, 2), ("=", 6, 3),
        ]

        for (text, r, c) in btns:
            b = tk.Button(master, text=text, command=lambda t=text: self.on_click(t), font=("Arial", 12), bd=0)
            b.grid(row=r, column=c, padx=6, pady=6, sticky="nsew")

        for i in range(4):
            master.grid_columnconfigure(i, weight=1)
        for i in range(1, 7):
            master.grid_rowconfigure(i, weight=1)

    def apply_theme(self, theme: dict):
        try:
            entry_bg = theme.get("entry_bg", "#ffffff")
            fg = theme.get("fg", "#232b36")
            self.entry.configure(bg=entry_bg, fg=fg)
        except Exception:
            pass

    def on_click(self, text):
        if text == "AC":
            self.entry.delete(0, tk.END)
            return
        if text == "=":
            self.evaluate()
            return
        if text in ("sin", "cos", "tan", "sqrt", "ln", "log", "!", "x^y"):
            self._apply_function(text)
            return
        # otherwise add to entry
        cur = self.entry.get()
        if cur == "0":
            self.entry.delete(0, tk.END)
            cur = ""
        self.entry.insert(tk.END, text)

    def _apply_function(self, name):
        val = self.entry.get().strip()
        if not val:
            return
        try:
            # allow expressions with ^ for power
            expr = val.replace('^', '**')
            base = float(eval(expr))
        except Exception as e:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, f"Error: invalid input")
            return

        try:
            if name == "sin":
                # treat input as degrees
                res = math.sin(math.radians(base))
            elif name == "cos":
                res = math.cos(math.radians(base))
            elif name == "tan":
                res = math.tan(math.radians(base))
            elif name == "sqrt":
                if base < 0:
                    raise ValueError("negative")
                res = math.sqrt(base)
            elif name == "ln":
                if base <= 0:
                    raise ValueError("non-positive")
                res = math.log(base)
            elif name == "log":
                if base <= 0:
                    raise ValueError("non-positive")
                res = math.log10(base)
            elif name == "!":
                n = int(base)
                if n < 0:
                    raise ValueError("negative")
                res = math.factorial(n)
            elif name == "x^y":
                # expect input like "base,exponent"
                if "," in val:
                    parts = val.split(",")
                    base = float(parts[0])
                    exp = float(parts[1])
                    res = base ** exp
                else:
                    # ask for exponent
                    exp = simpledialog.askfloat("Exponent", "Enter exponent:", parent=self.master)
                    if exp is None:
                        return
                    res = base ** exp
            else:
                return

            prec = int(self.settings.get("decimal_precision", 4)) if self.settings else 4
            if isinstance(res, float):
                out = f"{res:.{prec}f}"
            else:
                out = str(res)
            # show result
            self.entry.delete(0, tk.END)
            self.entry.insert(0, out)
            # log to history
            if self.history:
                self.history.add_entry(f"{name}({val}) = {out}")
        except ValueError:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, "Error: invalid input")
        except Exception as e:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, f"Error: {e}")

    def evaluate(self):
        expr = self.entry.get().strip()
        if not expr:
            return
        try:
            expr_eval = expr.replace('^', '**')
            result = eval(expr_eval)
            prec = int(self.settings.get("decimal_precision", 4)) if self.settings else 4
            if isinstance(result, float):
                out = f"{result:.{prec}f}"
            else:
                out = str(result)
            self.entry.delete(0, tk.END)
            self.entry.insert(0, out)
            if self.history:
                self.history.add_entry(f"{expr} = {out}")
        except ZeroDivisionError:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, "Error: Divide by zero")
        except Exception as e:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, "Error: invalid expression")
            return
