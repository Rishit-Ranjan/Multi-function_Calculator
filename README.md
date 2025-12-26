# Multi-Functional Calculator

A versatile desktop calculator application built with Python and Tkinter, combining multiple calculator types into a single, user-friendly, tabbed interface.

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

![1760074292759](image/README/1760074292759.png)<br/><br/>
**Tab 2: Area Calculator**

![1760074331592](image/README/1760074331592.png)<br/><br/>
**Tab 3: Programmable Calculator**

![1760074380687](image/README/1760074380687.png)


## How to Run

1. Clone the repository
2. Head over to dist folder and double click to run the main_app.exe.
3. It will run the python window application.

Note: No need to download python or Tkinter library.
    

## Code Structure

The project is organized into modular, class-based components for clarity and maintainability.

-   `main_app.py`: The main entry point for the application. It creates the main window and the tabbed notebook interface that houses the other calculators.
-   `standard_calculator.py`: Contains the `StandardCalculator` class, which defines the UI and logic for the standard arithmetic calculator.
-   `area_calculator.py`: Contains the `AreaCalculator` class. It provides a dynamic UI for selecting a shape and calculating its area in real-time.
-   `programmable_calculator.py`: Contains the `ProgrammableCalculator` class, which implements a simple Python environment for executing code.
