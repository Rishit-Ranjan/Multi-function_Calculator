import tkinter as tk

# Add a flag to track if last button pressed was '='
last_was_equal = False

def on_click(event):
    global last_was_equal
    text = event.widget["text"]
    if text == "=":
        try:
            result = str(eval(entry.get()))
            entry.delete(0, tk.END)
            entry.insert(tk.END, result)
            last_was_equal = True
        except Exception:
            entry.delete(0, tk.END)
            entry.insert(tk.END, "Error")
            last_was_equal = True
    elif text == "AC":
        entry.delete(0, tk.END)
        entry.insert(tk.END, "0")
        last_was_equal = False
    else:
        if entry.get() == "0" or entry.get() == "Error" or (last_was_equal and text.isdigit()):
            entry.delete(0, tk.END)
        if last_was_equal and text in "+-*/":
            last_was_equal = False
        elif last_was_equal:
            last_was_equal = False
        entry.insert(tk.END, text)

root = tk.Tk()
root.title("Calculator")
root.configure(bg="#f7f7f7")
root.resizable(False, False)

entry = tk.Entry(root, font=("Arial", 28), bg="#232b36", fg="white", bd=0, justify="right")
entry.insert(0, "0")
entry.grid(row=0, column=0, columnspan=4, padx=16, pady=(16, 8), sticky="we", ipady=20)

btn_cfg = {
    "font": ("Arial", 18, "bold"),
    "width": 4,
    "height": 2,
    "bd": 0,
    "relief": "flat",
}

buttons = [
    ("AC", 1, 0, "#ff5e5e", "white"),
    ("/", 1, 1, "#e6e8ec", "#232b36"),
    ("*", 1, 2, "#e6e8ec", "#232b36"),
    ("-", 1, 3, "#e6e8ec", "#232b36"),
    ("7", 2, 0, "#232b36", "white"),
    ("8", 2, 1, "#232b36", "white"),
    ("9", 2, 2, "#232b36", "white"),
    ("+", 2, 3, "#e6e8ec", "#232b36"),
    ("4", 3, 0, "#232b36", "white"),
    ("5", 3, 1, "#232b36", "white"),
    ("6", 3, 2, "#232b36", "white"),
    ("=", 3, 3, "#2ecc71", "white", 2),
    ("1", 4, 0, "#232b36", "white"),
    ("2", 4, 1, "#232b36", "white"),
    ("3", 4, 2, "#232b36", "white"),
    ("0", 5, 0, "#232b36", "white", 2),
    (".", 5, 2, "#232b36", "white"),
]

for btn in buttons:
    text, row, col, bg, fg = btn[:5]
    colspan = btn[5] if len(btn) > 5 else 1
    b = tk.Button(root, text=text, bg=bg, fg=fg, **btn_cfg)
    b.grid(row=row, column=col, columnspan=colspan, padx=6, pady=6, sticky="nsew")
    b.bind("<Button-1>", on_click)

# Make columns/rows expand equally
for i in range(4):
    root.grid_columnconfigure(i, weight=1)
for i in range(1, 6):
    root.grid_rowconfigure(i, weight=1)

root.mainloop()