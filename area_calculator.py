import tkinter as tk
from tkinter import ttk
import math

class AreaCalculator:
    def __init__(self, master, history=None, settings=None):
        self.master = master
        self.history = history
        self.settings = settings or {}
        master.configure(bg="#f7f7f7")
        
        # Configure grid for responsiveness
        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)

        # --- Main layout ---
        self.main_frame = tk.Frame(master, bg="#f7f7f7")
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # --- Shape Selection ---
        tk.Label(self.main_frame, text="Select a shape:", font=("Arial", 12), bg="#f7f7f7").grid(row=0, column=0, sticky="w", pady=(0, 5))
        self.shape_var = tk.StringVar()
        self.shape_selector = ttk.Combobox(self.main_frame, textvariable=self.shape_var, font=("Arial", 11), state="readonly")
        self.shapes = ('Circle', 'Triangle', 'Square', 'Rectangle')
        self.shape_selector['values'] = self.shapes
        self.shape_selector.grid(row=0, column=1, sticky="ew", pady=5)
        self.shape_selector.bind("<<ComboboxSelected>>", self.update_ui)
        self.main_frame.grid_columnconfigure(1, weight=1)

        # --- Dynamic Input Fields Frame ---
        self.input_frame = tk.Frame(self.main_frame, bg="#f7f7f7")
        self.input_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=10)
        self.input_frame.grid_columnconfigure(1, weight=1)

        # --- Result Display ---
        result_frame = tk.Frame(self.main_frame, bg="#f7f7f7")
        result_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=10)
        self.result_label = tk.Label(result_frame, text="Area: -", font=("Arial", 14, "bold"), bg="#f7f7f7")
        self.result_label.pack(side="left", padx=(0,8))

        # Save to history button
        self.save_btn = tk.Button(result_frame, text="Save", command=self.save_to_history, bg="#2ecc71", fg="white", bd=0)
        self.save_btn.pack(side="right")

        # --- Input widgets for each shape ---
        self.input_widgets = {}
        self.input_vars = {}
        self.create_input_fields()

        # Set a default selection
        self.shape_selector.set(self.shapes[0])
        self.update_ui()

    def create_input_fields(self):
        """Creates all possible input fields and hides them initially."""
        common_entry_config = {"font": ("Consolas", 12), "bg": "#e6e8ec", "bd": 0}
        common_label_config = {"font": ("Arial", 11), "bg": "#f7f7f7"}

        # Circle
        self.input_widgets['Circle'] = [
            (tk.Label(self.input_frame, text="Radius:", **common_label_config), tk.Entry(self.input_frame, **common_entry_config))
        ]
        # Triangle
        self.input_widgets['Triangle'] = [
            (tk.Label(self.input_frame, text="Base:", **common_label_config), tk.Entry(self.input_frame, **common_entry_config)),
            (tk.Label(self.input_frame, text="Height:", **common_label_config), tk.Entry(self.input_frame, **common_entry_config))
        ]
        # Square
        self.input_widgets['Square'] = [
            (tk.Label(self.input_frame, text="Side:", **common_label_config), tk.Entry(self.input_frame, **common_entry_config))
        ]
        # Rectangle
        self.input_widgets['Rectangle'] = [
            (tk.Label(self.input_frame, text="Length:", **common_label_config), tk.Entry(self.input_frame, **common_entry_config)),
            (tk.Label(self.input_frame, text="Width:", **common_label_config), tk.Entry(self.input_frame, **common_entry_config))
        ]

        # Bind calculation event to all entry widgets
        for shape in self.input_widgets:
            for _, entry in self.input_widgets[shape]:
                entry.bind("<KeyRelease>", self.calculate_area)

    def update_ui(self, event=None):
        """Hides all input fields and shows only the ones for the selected shape."""
        # Hide all widgets in the input frame
        for widget in self.input_frame.winfo_children():
            widget.grid_forget()

        shape = self.shape_var.get()
        if shape in self.input_widgets:
            for i, (label, entry) in enumerate(self.input_widgets[shape]):
                label.grid(row=i, column=0, sticky="w", padx=5, pady=5)
                entry.grid(row=i, column=1, sticky="ew", padx=5, pady=5)
                entry.delete(0, tk.END)

        self.input_frame.grid_columnconfigure(1, weight=1)
        self.input_frame.grid_rowconfigure(0, weight=1)
        self.calculate_area() # Reset/clear the area label

    def calculate_area(self, event=None):
        """Calculates the area based on the current inputs and updates the display."""
        shape = self.shape_var.get()
        area = None
        try:
            if shape == 'Circle':
                radius = float(self.input_widgets['Circle'][0][1].get())
                area = math.pi * radius**2
            elif shape == 'Triangle':
                base = float(self.input_widgets['Triangle'][0][1].get())
                height = float(self.input_widgets['Triangle'][1][1].get())
                area = 0.5 * base * height
            elif shape == 'Square':
                side = float(self.input_widgets['Square'][0][1].get())
                area = side**2
            elif shape == 'Rectangle':
                length = float(self.input_widgets['Rectangle'][0][1].get())
                width = float(self.input_widgets['Rectangle'][1][1].get())
                area = length * width

            if area is not None:
                prec = int(self.settings.get("decimal_precision", 4)) if self.settings else 4
                self.result_label.config(text=f"Area: {area:.{prec}f}")
            else:
                self.result_label.config(text="Area: -")

        except (ValueError, IndexError):
            # Empty or non-numeric input
            self.result_label.config(text="Area: - (incomplete)")
        except Exception as e:
            # Unexpected errors
            self.result_label.config(text=f"Error: {e}")
            if self.history:
                try:
                    self.history.add_entry(f"Area calc error: {e}")
                except Exception:
                    pass

    def save_to_history(self):
        if not self.history:
            return
        shape = self.shape_var.get()
        try:
            if shape == 'Circle':
                radius = self.input_widgets['Circle'][0][1].get()
                area_text = self.result_label.cget("text")
                self.history.add_entry(f"Circle radius={radius} -> {area_text}")
            elif shape == 'Triangle':
                base = self.input_widgets['Triangle'][0][1].get()
                height = self.input_widgets['Triangle'][1][1].get()
                area_text = self.result_label.cget("text")
                self.history.add_entry(f"Triangle base={base}, height={height} -> {area_text}")
            elif shape == 'Square':
                side = self.input_widgets['Square'][0][1].get()
                area_text = self.result_label.cget("text")
                self.history.add_entry(f"Square side={side} -> {area_text}")
            elif shape == 'Rectangle':
                length = self.input_widgets['Rectangle'][0][1].get()
                width = self.input_widgets['Rectangle'][1][1].get()
                area_text = self.result_label.cget("text")
                self.history.add_entry(f"Rectangle L={length}, W={width} -> {area_text}")
        except Exception:
            pass

    def apply_theme(self, theme: dict):
        try:
            bg = theme.get("bg", "#f7f7f7")
            fg = theme.get("fg", "#232b36")
            entry_bg = theme.get("entry_bg", "#ffffff")
            self.main_frame.configure(bg=bg)
            self.result_label.configure(bg=bg, fg=fg)
            try:
                self.save_btn.configure(bg=entry_bg, fg=fg)
            except Exception:
                pass
            for widgets in self.input_widgets.values():
                for label, entry in widgets:
                    try:
                        label.configure(bg=bg, fg=fg)
                        entry.configure(bg=entry_bg, fg=fg)
                    except Exception:
                        pass
        except Exception:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = AreaCalculator(root)
    root.mainloop()