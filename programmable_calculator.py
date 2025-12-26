import tkinter as tk

class ProgrammableCalculator:
    def __init__(self, master, history=None):
        self.master = master
        self.history = history
        master.configure(bg="#f7f7f7")

        self.user_env = {}

        self.display = tk.Text(master, height=10, width=40, font=("Consolas", 14), bg="#232b36", fg="white", bd=0)
        self.display.grid(row=0, column=0, columnspan=4, padx=10, pady=(10, 0))
        self.display.insert(tk.END, "Programmable Calculator\nType Python expressions or define functions.\nExample: def square(x): return x*x\nThen use: square(5)\n\n")

        self.input_var = tk.StringVar()
        self.input_entry = tk.Entry(master, textvariable=self.input_var, font=("Consolas", 16), bg="#e6e8ec", fg="#232b36", bd=0)
        self.input_entry.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="we")
        self.input_entry.bind("<Return>", self.evaluate)

        self.eval_btn = tk.Button(master, text="Evaluate", command=self.evaluate, font=("Arial", 14, "bold"), bg="#2ecc71", fg="white", bd=0, width=10)
        self.eval_btn.grid(row=1, column=3, padx=10, pady=10)

        self.clear_btn = tk.Button(master, text="Clear", command=self.clear_display, font=("Arial", 12), bg="#ff5e5e", fg="white", bd=0)
        self.clear_btn.grid(row=2, column=3, padx=10, pady=(0,10))

    def evaluate(self, event=None):
        expr = self.input_var.get()
        if not expr.strip():
            return
        self.display.insert(tk.END, f">>> {expr}\n")
        try:
            if expr.strip().startswith("def ") or "=" in expr:
                exec(expr, {}, self.user_env)
                self.display.insert(tk.END, "OK\n")
                if self.history:
                    self.history.add_entry(f"{expr} -> OK")
            else:
                result = eval(expr, {}, self.user_env)
                self.display.insert(tk.END, f"{result}\n")
                if self.history:
                    self.history.add_entry(f"{expr} = {result}")
        except ZeroDivisionError:
            msg = "Error: Division by zero"
            self.display.insert(tk.END, f"{msg}\n")
            if self.history:
                self.history.add_entry(f"{expr} -> {msg}")
        except SyntaxError:
            msg = "Error: Invalid expression"
            self.display.insert(tk.END, f"{msg}\n")
            if self.history:
                self.history.add_entry(f"{expr} -> {msg}")
        except Exception as e:
            msg = f"Error: {e}"
            self.display.insert(tk.END, f"{msg}\n")
            if self.history:
                self.history.add_entry(f"{expr} -> {msg}")
        self.display.see(tk.END)
        self.input_var.set("")

    def clear_display(self):
        self.display.delete(1.0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ProgrammableCalculator(root)
    root.mainloop()