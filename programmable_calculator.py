import tkinter as tk
import re
import math


class ProgrammableCalculator:
    def __init__(self, master, history=None, settings=None):
        self.master = master
        self.history = history
        self.settings = settings or {}
        master.configure(bg="#f7f7f7")

        self.user_env = {}

        # Configure grid to manage layout better
        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)

        # Main frame to hold display and input
        main_frame = tk.Frame(master, bg="#f7f7f7")
        main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # Display area (takes most space)
        display_label = tk.Label(main_frame, text="Output", font=("Arial", 10, "bold"), bg="#f7f7f7", fg="#232b36")
        display_label.grid(row=0, column=0, sticky="w", pady=(0, 5))

        self.display = tk.Text(main_frame, height=12, width=45, font=("Consolas", 11), bg="#232b36", fg="white", bd=1, relief="solid")
        self.display.grid(row=1, column=0, sticky="nsew", pady=(0, 10))
        self.display.insert(tk.END, "Programmable Calculator\nType Python expressions or define functions.\nExample: def square(x): return x*x\nThen use: square(5)\n\n")

        # Input label and entry
        input_label = tk.Label(main_frame, text="Input", font=("Arial", 10, "bold"), bg="#f7f7f7", fg="#232b36")
        input_label.grid(row=2, column=0, sticky="w", pady=(0, 5))

        self.input_entry = tk.Text(main_frame, height=3, width=45, font=("Consolas", 11), bg="#e6e8ec", fg="#232b36", bd=1, relief="solid")
        self.input_entry.grid(row=3, column=0, sticky="ew", pady=(0, 10))
        self.input_entry.bind("<Return>", self._on_enter)

        # Button frame
        btn_frame = tk.Frame(main_frame, bg="#f7f7f7")
        btn_frame.grid(row=4, column=0, sticky="ew")

        self.eval_btn = tk.Button(btn_frame, text="Evaluate", command=self.evaluate, font=("Arial", 11, "bold"), bg="#2ecc71", fg="white", bd=0, padx=12, pady=6, relief="flat")
        self.eval_btn.pack(side="left", padx=(0, 8))

        self.clear_btn = tk.Button(btn_frame, text="Clear Output", command=self.clear_display, font=("Arial", 11), bg="#ff5e5e", fg="white", bd=0, padx=12, pady=6, relief="flat")
        self.clear_btn.pack(side="left")

        # setup tags for basic syntax highlighting in the display
        self.display.tag_configure("kw", foreground="#ffb86b")
        self.display.tag_configure("num", foreground="#8be9fd")
        self.display.tag_configure("err", foreground="#ff6b6b")

    def _on_enter(self, event=None):
        # Prevent inserting a newline and run evaluate
        try:
            self.evaluate()
        finally:
            return "break"

    def _highlight_line(self, start_index):
        # Apply basic highlighting to the single line starting at start_index
        line = self.display.get(start_index, f"{start_index} lineend")
        # clear tags on that line
        self.display.tag_remove("kw", start_index, f"{start_index} lineend")
        self.display.tag_remove("num", start_index, f"{start_index} lineend")
        for m in re.finditer(r"\b(def|return|for|if|else|import|from|in|while|try|except|class)\b", line):
            s = f"{start_index}+{m.start()}c"
            e = f"{start_index}+{m.end()}c"
            self.display.tag_add("kw", s, e)
        for m in re.finditer(r"\b\d+\.?\d*\b", line):
            s = f"{start_index}+{m.start()}c"
            e = f"{start_index}+{m.end()}c"
            self.display.tag_add("num", s, e)

    def evaluate(self, event=None):
        expr = self.input_entry.get("1.0", "end").strip()
        if not expr:
            return
        # show input
        insert_index = self.display.index(tk.END)
        self.display.insert(tk.END, f">>> {expr}\n")
        try:
            # restricted builtins
            safe_builtins = {"abs": abs, "min": min, "max": max, "sum": sum, "round": round, "len": len}
            safe_globals = {"__builtins__": safe_builtins, "math": math}
            if expr.strip().startswith("def ") or "=" in expr:
                exec(expr, safe_globals, self.user_env)
                msg = "OK"
                self.display.insert(tk.END, f"{msg}\n")
                if self.history:
                    self.history.add_entry(f"{expr} -> {msg}")
            else:
                result = eval(expr, safe_globals, self.user_env)
                # format floats according to settings
                if isinstance(result, float) and self.settings and "decimal_precision" in self.settings:
                    prec = int(self.settings.get("decimal_precision", 4))
                    result_str = f"{result:.{prec}f}"
                else:
                    result_str = str(result)
                self.display.insert(tk.END, f"{result_str}\n")
                if self.history:
                    self.history.add_entry(f"{expr} = {result_str}")
        except ZeroDivisionError:
            msg = "Error: Division by zero"
            self.display.insert(tk.END, f"{msg}\n")
            self.display.tag_add("err", f"{insert_index}+1line", f"{insert_index}+1lineend")
            if self.history:
                self.history.add_entry(f"{expr} -> {msg}")
        except SyntaxError:
            msg = "Error: Invalid expression"
            self.display.insert(tk.END, f"{msg}\n")
            self.display.tag_add("err", f"{insert_index}+1line", f"{insert_index}+1lineend")
            if self.history:
                self.history.add_entry(f"{expr} -> {msg}")
        except Exception as e:
            msg = f"Error: {e}"
            self.display.insert(tk.END, f"{msg}\n")
            self.display.tag_add("err", f"{insert_index}+1line", f"{insert_index}+1lineend")
            if self.history:
                self.history.add_entry(f"{expr} -> {msg}")

        # basic highlight the input line we added
        try:
            # the input we added is at insert_index (start), so highlight that line
            self._highlight_line(insert_index)
        except Exception:
            pass

        self.display.see(tk.END)
        self.input_entry.delete("1.0", "end")

    def clear_display(self):
        self.display.delete(1.0, tk.END)

    def apply_theme(self, theme: dict):
        try:
            bg = theme.get("bg", "#f7f7f7")
            fg = theme.get("fg", "#232b36")
            entry_bg = theme.get("entry_bg", "#e6e8ec")
            display_bg = theme.get("entry_bg", "#232b36")
            
            self.master.configure(bg=bg)
            self.display.configure(bg=display_bg, fg="white" if theme.get("theme", "dark") == "dark" else "#232b36")
            self.input_entry.configure(bg=entry_bg, fg=fg)
            try:
                self.eval_btn.configure(bg=theme.get("accent", "#2ecc71"), fg="white")
                self.clear_btn.configure(bg="#ff5e5e", fg="white")
            except Exception:
                pass
        except Exception:
            pass


if __name__ == "__main__":
    root = tk.Tk()
    app = ProgrammableCalculator(root)
    root.mainloop()