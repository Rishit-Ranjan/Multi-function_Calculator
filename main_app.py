import tkinter as tk
from tkinter import ttk

# Import the calculator classes from their respective files
from standard_calculator import StandardCalculator
from area_calculator import AreaCalculator
from programmable_calculator import ProgrammableCalculator

class MainApplication:
    def __init__(self, master):
        self.master = master
        master.title("Multi-Function Calculator")
        master.geometry("450x550") # Adjusted for a good default size
        master.resizable(True, True)

        # Create a Notebook (tabbed interface)
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(pady=10, padx=10, expand=True, fill="both")

        # Create frames for each tab
        self.standard_calc_frame = tk.Frame(self.notebook, width=400, height=500)
        self.area_calc_frame = tk.Frame(self.notebook, width=400, height=500)
        self.prog_calc_frame = tk.Frame(self.notebook, width=400, height=500)

        self.standard_calc_frame.pack(fill="both", expand=True)
        self.area_calc_frame.pack(fill="both", expand=True)
        self.prog_calc_frame.pack(fill="both", expand=True)

        # Add frames to the notebook
        self.notebook.add(self.standard_calc_frame, text="Standard")
        self.notebook.add(self.area_calc_frame, text="Area")
        self.notebook.add(self.prog_calc_frame, text="Programmable")

        # Instantiate each calculator into its respective frame
        StandardCalculator(self.standard_calc_frame)
        AreaCalculator(self.area_calc_frame)
        ProgrammableCalculator(self.prog_calc_frame)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()