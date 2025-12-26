# Multi-Function Calculator

A versatile desktop calculator application built with Python and Tkinter, combining multiple calculator types into a single, user-friendly, tabbed interface.

[![Download](https://img.shields.io/badge/Download-Windows_EXE-blue)](../../releases)

## Features

- **Unified Interface:** A clean, tabbed layout to easily switch between different calculator modes.
- **Standard Calculator:** For all your day-to-day arithmetic needs. Features a modern design with clear buttons and a responsive display.
- **Area Calculator:** A handy tool for students and professionals. Quickly calculate the area of various geometric shapes:
    - Circle
    - Triangle
    - Square
    - Rectangle
- **Programmable Calculator:** A mini Python REPL (Read-Eval-Print Loop) that allows you to:
    - Execute multi-line Python expressions.
    - Define and use variables.
    - Create and call your own functions.

## Screenshots

**Tab 1: Standard Calculator**

<img width="661" height="727" alt="image" src="https://github.com/user-attachments/assets/c189d2ad-0e15-4dbc-b7d8-de6252a3e85f" /><br/><br/>
**Tab 2: Area Calculator**

<img width="661" height="727" alt="image" src="https://github.com/user-attachments/assets/fa3d4052-b17e-4957-b853-08716e9176d6" /><br/><br/>
**Tab 3: Programmable Calculator**

<img width="661" height="727" alt="image" src="https://github.com/user-attachments/assets/2ad9054c-9e40-4f77-bb5c-6678cc684d65" /><br/><br/>

**Tab 4: Scientific Calculator**
<img width="661" height="727" alt="image" src="https://github.com/user-attachments/assets/143dda36-6122-4c98-92e9-d5df6cf49d8a" />


## How to Run (Windows)

1. Go to the **Releases** section of this repository.
2. Download the latest `main_app.exe`.
3. Double-click the `.exe` file to launch the application.

> **Note:** No need to install Python or Tkinter. Everything is bundled inside the executable.

## Code Structure

The project is organized into modular, class-based components for clarity and maintainability.

-   `main_app.py`: The main entry point for the application. It creates the main window and the tabbed notebook interface that houses the other calculators.
-   `standard_calculator.py`: Contains the `StandardCalculator` class, which defines the UI and logic for the standard arithmetic calculator.
-   `area_calculator.py`: Contains the `AreaCalculator` class. It provides a dynamic UI for selecting a shape and calculating its area in real-time.
-   `programmable_calculator.py`: Contains the `ProgrammableCalculator` class, which implements a simple Python environment for executing code.

**Build**
python -m PyInstaller --onefile --windowed main_app.py
