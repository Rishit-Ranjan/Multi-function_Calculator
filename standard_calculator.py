import tkinter as tk

class StandardCalculator:
    def __init__(self, master):
        self.master = master
        master.configure(bg="#f7f7f7")

        # Flag to track if the last operation was an evaluation
        self.last_was_equal = False

        self.entry = tk.Entry(master, font=("Arial", 28), bg="#232b36", fg="white", bd=0, justify="right")
        self.entry.insert(0, "0")
        self.entry.grid(row=0, column=0, columnspan=4, padx=16, pady=(16, 8), sticky="we", ipady=20)

        self.create_buttons()

        # Make columns/rows expand equally
        for i in range(4):
            master.grid_columnconfigure(i, weight=1)
        for i in range(1, 6):
            master.grid_rowconfigure(i, weight=1)

    def on_click(self, event):
        text = event.widget["text"]
        if text == "=":
            try:
                result = str(eval(self.entry.get()))
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, result)
                self.last_was_equal = True
            except Exception:
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, "Error")
                self.last_was_equal = True
        elif text == "AC":
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, "0")
            self.last_was_equal = False
        else:
            if self.entry.get() == "0" or self.entry.get() == "Error" or (self.last_was_equal and text.isdigit()):
                self.entry.delete(0, tk.END)
            
            if self.last_was_equal:
                self.last_was_equal = False
            
            self.entry.insert(tk.END, text)

    def create_buttons(self):
        btn_cfg = {
            "font": ("Arial", 18, "bold"), "width": 4, "height": 2,
            "bd": 0, "relief": "flat",
        }

        buttons = [
            ("AC", 1, 0, "#ff5e5e", "white"), ("/", 1, 1, "#e6e8ec", "#232b36"),
            ("*", 1, 2, "#e6e8ec", "#232b36"), ("-", 1, 3, "#e6e8ec", "#232b36"),
            ("7", 2, 0, "#232b36", "white"), ("8", 2, 1, "#232b36", "white"),
            ("9", 2, 2, "#232b36", "white"), ("+", 2, 3, "#e6e8ec", "#232b36"),
            ("4", 3, 0, "#232b36", "white"), ("5", 3, 1, "#232b36", "white"),
            ("6", 3, 2, "#232b36", "white"), ("=", 3, 3, "#2ecc71", "white", 2),
            ("1", 4, 0, "#232b36", "white"), ("2", 4, 1, "#232b36", "white"),
            ("3", 4, 2, "#232b36", "white"), ("0", 5, 0, "#232b36", "white", 2),
            (".", 5, 2, "#232b36", "white"),
        ]

        for btn_data in buttons:
            text, row, col, bg, fg = btn_data[:5]
            colspan = btn_data[5] if len(btn_data) > 5 else 1
            rowspan = 2 if text == "=" else 1
            
            b = tk.Button(self.master, text=text, bg=bg, fg=fg, **btn_cfg)
            b.grid(row=row, column=col, columnspan=colspan, rowspan=rowspan, padx=6, pady=6, sticky="nsew")
            b.bind("<Button-1>", self.on_click)

if __name__ == "__main__":
    root = tk.Tk()
    app = StandardCalculator(root)
    root.mainloop()