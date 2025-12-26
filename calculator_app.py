import json
import os
import tkinter as tk
from tkinter import ttk

# Import the calculator classes from their respective files
from standard_calculator import StandardCalculator
from area_calculator import AreaCalculator
from programmable_calculator import ProgrammableCalculator
from history_store import CalculationHistory
from scientific_calculator import ScientificCalculator
import logging

LOG_FILE = os.path.join(os.path.dirname(__file__), "app.log")
HISTORY_FILE = os.path.join(os.path.dirname(__file__), "history.json")
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s %(levelname)s:%(message)s")

SETTINGS_FILE = os.path.join(os.path.dirname(__file__), "settings.json")

DEFAULT_SETTINGS = {
    "theme": "dark",
    "decimal_precision": 4,
    "clear_history_on_exit": False
}

class MainApplication:
    def __init__(self, master):
        self.master = master
        master.title("Multi-Function Calculator")
        master.geometry("450x550") # Adjusted for a good default size
        master.resizable(True, True)

        # Load settings
        self.settings = self._load_settings()

        # Top control bar
        self.topbar = tk.Frame(master, bg="#232b36")
        self.topbar.pack(fill="x", padx=0, pady=0)

        self.theme_btn = tk.Button(self.topbar, text="Toggle Theme", command=self.toggle_theme, bd=0, font=("Arial", 10), bg="#2ecc71", fg="white", padx=10, pady=6, relief="flat")
        self.theme_btn.pack(side="left", padx=5, pady=5)

        self.settings_btn = tk.Button(self.topbar, text="Settings", command=self.open_settings, bd=0, font=("Arial", 10), bg="#2ecc71", fg="white", padx=10, pady=6, relief="flat")
        self.settings_btn.pack(side="left", padx=5, pady=5)

        # Create a Notebook (tabbed interface) with modern styling
        self.style = ttk.Style()
        self._apply_notebook_style(self.settings.get("theme", "dark"))
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(pady=8, padx=8, expand=True, fill="both")

        # Create frames for each tab
        self.standard_calc_frame = tk.Frame(self.notebook, width=400, height=500)
        self.area_calc_frame = tk.Frame(self.notebook, width=400, height=500)
        self.prog_calc_frame = tk.Frame(self.notebook, width=400, height=500)
        self.scientific_calc_frame = tk.Frame(self.notebook, width=400, height=500)
        self.history_frame = tk.Frame(self.notebook, width=400, height=500)

        self.standard_calc_frame.pack(fill="both", expand=True)
        self.area_calc_frame.pack(fill="both", expand=True)
        self.prog_calc_frame.pack(fill="both", expand=True)
        self.scientific_calc_frame.pack(fill="both", expand=True)
        self.history_frame.pack(fill="both", expand=True)

        # Add frames to the notebook
        self.notebook.add(self.standard_calc_frame, text="Standard")
        self.notebook.add(self.area_calc_frame, text="Area")
        self.notebook.add(self.prog_calc_frame, text="Programmable")
        self.notebook.add(self.scientific_calc_frame, text="Scientific")
        self.notebook.add(self.history_frame, text="History")

        # Instantiate the shared history manager and calculators
        self.history = CalculationHistory(self.history_frame, history_file=HISTORY_FILE, max_entries=50)

        # Create instances and keep references for theme/setting updates
        self.standard_calc = StandardCalculator(self.standard_calc_frame, history=self.history, settings=self.settings)
        self.area_calc = AreaCalculator(self.area_calc_frame, history=self.history, settings=self.settings)
        self.prog_calc = ProgrammableCalculator(self.prog_calc_frame, history=self.history, settings=self.settings)
        self.scientific_calc = ScientificCalculator(self.scientific_calc_frame, history=self.history, settings=self.settings)

        # Apply initial theme
        self.apply_theme(self.settings.get("theme", "dark"))

        # Handle exit (clear history on exit setting)
        master.protocol("WM_DELETE_WINDOW", self.on_close)
        logging.info("Application initialized")

    def _load_settings(self):
        try:
            if os.path.exists(SETTINGS_FILE):
                with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    DEFAULT_SETTINGS.update(data)
            return DEFAULT_SETTINGS.copy()
        except Exception:
            return DEFAULT_SETTINGS.copy()

    def _save_settings(self):
        try:
            with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
                json.dump(self.settings, f, indent=2)
        except Exception:
            pass

    def _apply_notebook_style(self, theme_name: str):
        """Apply modern tab styling based on theme"""
        if theme_name == "light":
            bg = "#f7f7f7"
            fg = "#232b36"
            selected_bg = "#ffffff"
            active_fg = "#2ecc71"
        else:
            bg = "#232b36"
            fg = "#f7f7f7"
            selected_bg = "#2b3036"
            active_fg = "#2ecc71"

        self.style.theme_use('clam')
        self.style.configure('TNotebook', background=bg, borderwidth=0)
        self.style.configure('TNotebook.Tab', padding=[15, 8], font=('Arial', 10, 'bold'))
        self.style.map('TNotebook.Tab',
                      background=[("selected", selected_bg), ("!selected", bg)],
                      foreground=[("selected", active_fg), ("!selected", fg)])

    def toggle_theme(self):
        current = self.settings.get("theme", "dark")
        new = "light" if current == "dark" else "dark"
        self.settings["theme"] = new
        self._save_settings()
        self.apply_theme(new)

    def apply_theme(self, theme_name: str):
        # Basic theme application: set colors and notify calculators/history
        if theme_name == "light":
            theme = {"bg": "#f7f7f7", "fg": "#232b36", "accent": "#2ecc71", "entry_bg": "#ffffff"}
        else:
            theme = {"bg": "#232b36", "fg": "#f7f7f7", "accent": "#2ecc71", "entry_bg": "#2b3036"}

        # Apply notebook style
        self._apply_notebook_style(theme_name)

        self.master.configure(bg=theme["bg"])
        # update topbar
        try:
            self.topbar.configure(bg=theme["bg"])
            self.theme_btn.configure(bg=theme["accent"], fg="white")
            self.settings_btn.configure(bg=theme["accent"], fg="white")
        except Exception:
            pass

        # Propagate theme
        try:
            self.standard_calc.apply_theme(theme)
            self.area_calc.apply_theme(theme)
            self.prog_calc.apply_theme(theme)
            try:
                self.scientific_calc.apply_theme(theme)
            except Exception:
                pass
            self.history.apply_theme(theme)
        except Exception:
            pass

    def open_settings(self):
        # Simple settings dialog
        dlg = tk.Toplevel(self.master)
        dlg.title("Settings")
        dlg.transient(self.master)

        tk.Label(dlg, text="Default Theme:").grid(row=0, column=0, sticky="w", padx=8, pady=8)
        theme_var = tk.StringVar(value=self.settings.get("theme", "dark"))
        tk.OptionMenu(dlg, theme_var, "dark", "light").grid(row=0, column=1, padx=8, pady=8)

        tk.Label(dlg, text="Decimal precision:").grid(row=1, column=0, sticky="w", padx=8, pady=8)
        prec_var = tk.IntVar(value=self.settings.get("decimal_precision", 4))
        tk.Spinbox(dlg, from_=0, to=10, textvariable=prec_var, width=5).grid(row=1, column=1, padx=8, pady=8)

        clear_var = tk.BooleanVar(value=self.settings.get("clear_history_on_exit", False))
        tk.Checkbutton(dlg, text="Clear history on exit", variable=clear_var).grid(row=2, column=0, columnspan=2, padx=8, pady=8)

        def save_and_close():
            self.settings["theme"] = theme_var.get()
            self.settings["decimal_precision"] = int(prec_var.get())
            self.settings["clear_history_on_exit"] = bool(clear_var.get())
            self._save_settings()
            self.apply_theme(self.settings["theme"])
            dlg.destroy()

        tk.Button(dlg, text="Save", command=save_and_close, bg="#2ecc71", fg="white").grid(row=3, column=0, columnspan=2, pady=8)

    def on_close(self):
        try:
            if self.settings.get("clear_history_on_exit") and self.history:
                self.history.clear()
            # ensure saved
            try:
                self.history._save()
            except Exception:
                pass
            logging.info("Application exiting")
        except Exception:
            pass
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()