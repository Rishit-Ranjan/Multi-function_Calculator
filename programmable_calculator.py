import tkinter as tk

class ProgrammableCalculator:
    def __init__(self, master):
        self.master = master
        master.title("Programmable Calculator")
        master.configure(bg="#f7f7f7")
        master.resizable(False, False)

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
            else:
                result = eval(expr, {}, self.user_env)
                self.display.insert(tk.END, f"{result}\n")
        except Exception as e:
            self.display.insert(tk.END, f"Error: {e}\n")
        self.display.see(tk.END)
        self.input_var.set("")

    def clear_display(self):
        self.display.delete(1.0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ProgrammableCalculator(root)
    root.mainloop()